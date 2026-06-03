from django.views.generic import TemplateView
from django.http import Http404
from django.core.cache import cache
from apps.core.db import (
    get_solutions, get_solution_detail,
    get_solution_products, increment_solution_views,
)
 
 
class SolutionListView(TemplateView):
    template_name = "solutions/list.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        req = self.request
 
        category_slug = (
            self.kwargs.get("category_slug")
            or req.GET.get("category")
            or None
        )

        limit  = 12
        page   = max(1, int(req.GET.get("page", 1)))
        offset = (page - 1) * limit
 
        solutions, total = get_solutions(
            category_slug = category_slug,
            limit  = limit,
            offset = offset,
        )

        from apps.solutions.models import SolutionCategory
        solutions_categories = cache.get_or_set(
            "solution_categories_nav",
            lambda: list(SolutionCategory.objects.filter(is_active=True).values("name", "slug").order_by("sort_order")),
            timeout=900,
        )

        context.update({
            "solutions":      solutions,
            "total":          total,
            "active_category": category_slug,
            "solution_categories": solutions_categories,
            "page":           page,
            "has_next":       total > page * limit,
            "has_previous":   page > 1,
        })
        return context
 
 
class SolutionDetailView(TemplateView):
    template_name = "solutions/detail.html"
 
    def get(self, request, slug, *args, **kwargs):
        self.slug = slug
        response = super().get(request, *args, **kwargs)
        sol = self._get_solution()
        if sol:
            from apps.solutions.tasks import increment_solution_views_task
            increment_solution_views_task.delay(sol["id"])
        return response
 
    def _get_solution(self):
        cache_key = f"solution_detail_{self.slug}"
        sol = cache.get(cache_key)
        if not sol:
            sol = get_solution_detail(self.slug)
            if sol:
                cache.set(cache_key, sol, 300)
        return sol
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solution = self._get_solution()
 
        if not solution:
            raise Http404("Giải pháp không tồn tại")
 
        # Parse JSON fields if they are strings
        import json
        for field in ["pain_points", "benefits"]:
            val = solution.get(field)
            if isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    solution[field] = parsed if isinstance(parsed, list) else [parsed]
                except (json.JSONDecodeError, TypeError):
                    solution[field] = [val]

        # Lấy sản phẩm thuộc giải pháp
        all_products      = get_solution_products(solution["id"], featured_only=False)
        featured_products = [p for p in all_products if p.get("is_featured")]
        
        from apps.solutions.models import ArchitectureBlock, WorkflowStep
        architecture_blocks = ArchitectureBlock.objects.filter(
            solution_id=solution["id"]
        ).order_by("sort_order")
 
        workflow_steps = WorkflowStep.objects.filter(
            solution_id=solution["id"]
        ).order_by("step_number")

        context.update({
            "solution":          solution,
            "all_products":      all_products,
            "featured_products": featured_products,
            "architecture_blocks": architecture_blocks,
            "workflow_steps":      workflow_steps,
        })
        return context
 
 