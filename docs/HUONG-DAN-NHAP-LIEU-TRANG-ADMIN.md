# HƯỚNG DẪN NHẬP LIỆU VÀ QUẢN TRỊ NỘI DUNG WEBSITE GREENTECH

> Tài liệu dành cho người quản trị nội dung website.  
> Phạm vi: các mục hiện có tại `/admin/`.  
> Cập nhật theo mã nguồn ngày 06/08/2026.

## 1. Mục đích của tài liệu

Tài liệu này giải thích:

- Mỗi mục trong trang quản trị dùng để làm gì.
- Mỗi ô cần nhập nội dung gì và nhập theo định dạng nào.
- Các lựa chọn như **Xuất bản**, **Nổi bật**, **Giá cố định** hoặc **Yêu cầu báo giá** có tác dụng gì.
- Dữ liệu sau khi lưu sẽ xuất hiện ở vị trí nào trên website.
- Những trường đang được lưu trong hệ thống nhưng giao diện công khai hiện chưa hiển thị trực tiếp.

Địa chỉ trang quản trị:

```text
https://ten-mien-cua-website/admin/
```

Khi chạy trên máy phát triển:

```text
http://127.0.0.1:8000/admin/
```

## 2. Các thao tác chung trong trang admin

### 2.1. Các nút lưu

| Nút | Tác dụng |
|---|---|
| **Lưu** | Lưu dữ liệu và quay lại danh sách. |
| **Lưu và tiếp tục chỉnh sửa** | Lưu nhưng vẫn ở lại trang hiện tại để tiếp tục nhập. Nên dùng khi phải tải nhiều ảnh hoặc tài liệu. |
| **Lưu và thêm mới** | Lưu bản ghi hiện tại rồi mở biểu mẫu tạo bản ghi tiếp theo. |
| **Xóa** | Xóa bản ghi. Chỉ sử dụng khi chắc chắn vì dữ liệu liên quan có thể bị ảnh hưởng. |

Sau khi sửa nội dung đang hiển thị công khai, nên mở trang tương ứng bằng cửa sổ riêng tư và tải lại để kiểm tra.

### 2.2. Các trường dùng chung

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Slug** | Chữ thường, không dấu, dùng dấu gạch ngang. Ví dụ: `cam-bien-nhiet-do-do-am`. | Tạo phần cuối của đường dẫn trang. Ví dụ: `/products/cam-bien-nhiet-do-do-am/`. Trường thường được tự tạo từ tên hoặc tiêu đề. |
| **Status / Trạng thái** | Chọn một trong ba trạng thái. | Quyết định nội dung có được công khai hay không. |
| **Published at / Thời gian xuất bản** | Chọn ngày và giờ. | Ngày xuất bản hiển thị trên bài viết và dùng để sắp xếp một số loại nội dung. |
| **Is featured / Nổi bật** | Đánh dấu hoặc bỏ đánh dấu. | Cho phép nội dung xuất hiện tại khu vực nổi bật trên trang chủ hoặc đầu danh sách, tùy từng loại nội dung. |
| **Sort order / Thứ tự** | Nhập số nguyên không âm. | Số nhỏ được ưu tiên trước. Nên dùng `10, 20, 30...` để dễ chèn thêm mục ở giữa. |
| **Created at / Updated at** | Hệ thống tự tạo. | Cho biết thời điểm tạo và cập nhật; không cần nhập. |
| **View count / Lượt xem** | Hệ thống tự tăng. | Dùng cho thống kê và hiển thị số lượt xem. Không nên sửa thủ công. |

Ý nghĩa của trạng thái xuất bản:

| Trạng thái | Hiển thị công khai | Khi nào sử dụng |
|---|---:|---|
| **Draft** | Không | Nội dung đang soạn hoặc chưa được duyệt. |
| **Published** | Có | Nội dung đã hoàn chỉnh và được phép xuất hiện trên website. |
| **Archived** | Không | Nội dung cũ cần giữ trong hệ thống nhưng không muốn xóa. |

Lưu ý: chọn **Published** không tự bảo đảm nội dung đã đầy đủ. Trước khi xuất bản cần kiểm tra ảnh, mô tả, giá, liên kết và ngày xuất bản.

### 2.3. Cách nhập nội dung trong CKEditor

Các trường như **Mô tả chi tiết**, **Tổng quan giải pháp** và **Nội dung bài viết** sử dụng CKEditor.

Quy tắc nên áp dụng:

- Dùng menu **Định dạng** cho tiêu đề, không tự tăng kích thước chữ bằng nhiều khoảng trắng.
- Dùng nút danh sách có dấu chấm hoặc danh sách đánh số để tạo các đầu dòng.
- Không tự gõ dấu `+` hoặc `-` cho từng dòng nếu muốn có danh sách chuẩn.
- Không chèn dòng trống giữa mọi đầu dòng. Nhấn `Enter` một lần để tạo mục tiếp theo.
- Chỉ dùng **Mã HTML** khi người nhập hiểu HTML.
- Không sao chép trực tiếp nội dung có định dạng phức tạp từ Word. Nếu cần, hãy dán dưới dạng văn bản thuần rồi định dạng lại.

Ví dụ nội dung hợp lệ:

```text
Trạm giám sát lưu lượng khí

• Số lượng kênh đo: 01 kênh
• Tự động điều khiển theo lưu lượng đặt
• Nguồn cấp: 220 VAC / 50 Hz
• Truyền dữ liệu qua mạng viễn thông
```

### 2.4. Quy tắc dùng ảnh và tệp

- Ảnh nên dùng `JPG`, `PNG` hoặc `WebP`; logo có thể dùng `SVG` nếu vị trí đó hỗ trợ.
- Tên tệp nên không dấu, không có ký tự đặc biệt. Ví dụ: `cam-bien-nhiet-do-mat-truoc.jpg`.
- Ảnh sản phẩm nên có nền sạch và tỷ lệ vuông.
- Ảnh giải pháp và ảnh bài viết nên ưu tiên tỷ lệ ngang `16:9`.
- Ảnh triển khai thực tế nên ưu tiên tỷ lệ `3:2` hoặc `4:3`.
- Tài liệu sản phẩm nên ưu tiên PDF.
- Không tải ảnh có dung lượng quá lớn nếu không cần thiết. Khuyến nghị dưới 2 MB mỗi ảnh.
- Ảnh và tài liệu tải từ admin thuộc dữ liệu **media**, không nằm trong Git. Khi chuyển máy chủ phải sao lưu cả cơ sở dữ liệu và thư mục/volume media.

## 3. Thứ tự nhập dữ liệu được khuyến nghị

Khi tạo mới nội dung, nên thực hiện theo thứ tự:

1. Tạo **Danh mục** và **Thương hiệu**.
2. Tạo **Sản phẩm**.
3. Tạo **Danh mục giải pháp**.
4. Tạo **Giải pháp**, sau đó gắn sản phẩm và ảnh triển khai.
5. Tạo **Dự án khách hàng** nếu có.
6. Tạo **Danh mục bài viết** và **Bài viết**.
7. Xem lại ngoài website rồi mới chuyển trạng thái sang **Published**.

## 4. Nhóm “Danh mục và thương hiệu”

### 4.1. Danh mục

Đường dẫn admin: **Danh mục và thương hiệu → Danh mục**.

Danh mục dùng để phân nhóm sản phẩm và tạo bộ lọc trên trang sản phẩm.

| Trường | Cách nhập | Tác dụng và vị trí hiển thị |
|---|---|---|
| **Name** | Tên ngắn gọn, ví dụ `Cảm biến môi trường`. | Hiển thị trong bộ lọc, breadcrumb và danh mục của sản phẩm. |
| **Slug** | Để hệ thống tự tạo hoặc nhập `cam-bien-moi-truong`. | Dùng trong liên kết lọc sản phẩm. |
| **Danh mục cha** | Để trống nếu là danh mục cấp cao; chọn một danh mục nếu là mục con. | Tạo cấu trúc cây và giúp nhóm sản phẩm theo cấp. |
| **Description** | Mô tả ngắn về nhóm sản phẩm. | Được lưu để mô tả danh mục; giao diện sản phẩm hiện chưa hiển thị rõ phần này. |
| **Thumbnail** | Ảnh đại diện danh mục. | Được lưu cho danh mục; giao diện danh sách hiện tại chưa sử dụng trực tiếp ở khu vực chính. |
| **Icon class** | Tên lớp CSS của biểu tượng. | Trường nâng cao; hiện chưa được sử dụng trực tiếp trên trang danh sách sản phẩm. Có thể để trống. |
| **Low stock threshold** | Số nguyên, ví dụ `10`. | Khi tồn kho của sản phẩm trong danh mục nhỏ hơn hoặc bằng ngưỡng, sản phẩm có thể chuyển sang trạng thái **Sắp hết** khi hệ thống tính lại tồn kho. |
| **Is active** | Đánh dấu nếu danh mục đang sử dụng. | Danh mục không kích hoạt sẽ bị loại khỏi các danh sách công khai có lọc trạng thái hoạt động. |
| **Show in nav** | Đánh dấu nếu muốn có trong điều hướng. | Cho phép danh mục được dùng trong vùng điều hướng có hỗ trợ trường này. |
| **Sort order** | Ví dụ `10`, `20`, `30`. | Quy định thứ tự danh mục. |
| **SEO** | Nhập tiêu đề, mô tả và từ khóa. | Thông tin phục vụ công cụ tìm kiếm; không hiển thị như nội dung thông thường. |

Ví dụ:

```text
Name: Cảm biến môi trường
Slug: cam-bien-moi-truong
Danh mục cha: Thiết bị đo lường
Low stock threshold: 5
Is active: Có
Show in nav: Có
Sort order: 20
```

### 4.2. Thương hiệu

Đường dẫn admin: **Danh mục và thương hiệu → Thương hiệu**.

| Trường | Cách nhập | Tác dụng và vị trí hiển thị |
|---|---|---|
| **Tên** | Tên chính thức của hãng. | Hiển thị trên thẻ sản phẩm và trang thương hiệu. |
| **Slug** | Ví dụ `siemens`. | Tạo URL trang thương hiệu. |
| **Logo** | Ảnh logo rõ, nền trong suốt nếu có thể. | Hiển thị ở trang thương hiệu và khu vực thương hiệu nổi bật. |
| **Website** | URL đầy đủ, ví dụ `https://www.siemens.com/`. | Tạo liên kết tới website hãng trên trang thương hiệu. |
| **Mô tả** | Giới thiệu ngắn về hãng. | Hiển thị trên trang chi tiết thương hiệu. |
| **Quốc gia** | Ví dụ `Đức`. | Hiển thị trên trang thương hiệu. |
| **Kích hoạt** | Đánh dấu khi thương hiệu còn sử dụng. | Dùng để lọc thương hiệu hoạt động ở các khu vực công khai. |
| **Nổi bật** | Đánh dấu cho thương hiệu quan trọng. | Hiển thị trong khu vực thương hiệu nổi bật ở trang chủ và thanh thương hiệu. |
| **Sort order** | Số nhỏ đứng trước. | Sắp xếp thương hiệu. |

## 5. Nhóm “Sản phẩm”

### 5.1. Tạo hoặc sửa sản phẩm

Đường dẫn admin: **Sản phẩm → Sản phẩm**.

#### A. Thông tin cơ bản

| Trường | Cách nhập | Tác dụng và vị trí hiển thị |
|---|---|---|
| **Tên sản phẩm** | Tên đầy đủ, dễ tìm kiếm. | Tiêu đề thẻ sản phẩm, trang chi tiết, breadcrumb và kết quả tìm kiếm. |
| **Slug** | Để tự sinh từ tên rồi kiểm tra lại. | Tạo URL `/products/<slug>/`. Không nên đổi sau khi đã chia sẻ liên kết. |
| **SKU** | Mã duy nhất, ví dụ `GTC-AIR-01`. | Hiển thị trên thẻ và trang chi tiết; dùng để tìm kiếm và lưu lịch sử đơn hàng. Không được trùng. |
| **Mã linh kiện** | Mã do nhà sản xuất cung cấp. | Dùng để quản lý và tìm kiếm trong admin; hiện không phải thông tin nổi bật ngoài website. |
| **Danh mục** | Chọn một danh mục đã tạo. | Hiển thị trong breadcrumb và dùng để lọc sản phẩm. Bắt buộc. |
| **Thương hiệu** | Chọn hãng hoặc để trống. | Hiển thị cạnh SKU và liên kết sản phẩm với trang thương hiệu. |

#### B. Ảnh đại diện

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Ảnh đại diện** | Ảnh vuông, khuyến nghị tối thiểu `800 × 800 px`. | Hiển thị tại trang chủ, danh sách, giỏ hàng và dùng làm ảnh dự phòng trên trang chi tiết. |
| **Ảnh hiện tại** | Chỉ xem. | Xem trước ảnh đang lưu. |

#### C. Giá bán

| Loại giá | Cách nhập | Kết quả ngoài website |
|---|---|---|
| **Giá cố định** | Nhập **Giá niêm yết**; nếu giảm giá thì nhập thêm **Giá khuyến mãi** nhỏ hơn giá niêm yết. | Hiển thị giá bằng VND, phần trăm giảm nếu hợp lệ và cho phép thêm vào giỏ hàng. |
| **Yêu cầu báo giá** | Để trống giá và giá khuyến mãi. | Không hiển thị `0 ₫`; hiển thị trạng thái báo giá và đưa khách sang luồng yêu cầu báo giá. |
| **Liên hệ để biết giá** | Để trống giá. | Hiển thị lời mời liên hệ và dẫn khách tới trang liên hệ thay vì mua trực tiếp. |

Các trường liên quan:

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Giá niêm yết** | Chỉ nhập số, ví dụ `12500000`. | Giá gốc. Không nhập dấu chấm hoặc chữ `đ`. |
| **Giá khuyến mãi** | Ví dụ `11000000`; để trống nếu không giảm. | Được dùng làm giá bán thực tế. Chỉ tạo giảm giá khi nhỏ hơn giá niêm yết. |
| **SL đặt hàng tối thiểu** | Số nguyên từ 1 trở lên. | Hiển thị số lượng tối thiểu và giới hạn số lượng khách có thể đặt. |

Không kết hợp tùy tiện **Yêu cầu báo giá** với giá số. Với sản phẩm có giá cố định nhưng đôi khi khách muốn hỏi thêm, giữ loại **Giá cố định**; chỉ dùng **Bắt buộc báo giá** khi thật sự không cho phép đặt hàng trực tiếp.

#### D. Tồn kho

| Trường | Cách nhập | Kết quả hiển thị |
|---|---|---|
| **Tình trạng kho** | Chọn Còn hàng, Sắp hết, Hết hàng hoặc Đặt trước. | Hiển thị nhãn tồn kho trên thẻ và trang chi tiết. Hết hàng sẽ chặn thao tác mua trực tiếp. |
| **Số lượng tồn** | Số nguyên từ 0 trở lên. | Khi trạng thái **Sắp hết**, website có thể hiển thị số lượng còn lại. |

Nên bảo đảm trạng thái và số lượng khớp nhau. Ví dụ: số lượng `0` thì không nên chọn **Còn hàng**.

#### E. Nội dung

| Trường | Cách nhập | Tác dụng và vị trí hiển thị |
|---|---|---|
| **Mô tả ngắn** | Tối đa 500 ký tự. Có thể nhập mỗi ý trên một dòng và bắt đầu bằng `-`. | Hiển thị cạnh ảnh và giá trên trang chi tiết; xuống dòng được giữ nguyên. Đồng thời được dùng làm mô tả SEO mặc định. |
| **Mô tả chi tiết** | Nhập bằng CKEditor, dùng tiêu đề, đoạn văn, danh sách và bảng. | Hiển thị trong tab **Mô tả** của trang sản phẩm. |
| **Tính năng nổi bật** | Mỗi tính năng một dòng, không cần nhập JSON. | Hệ thống lưu thành danh sách. Giao diện sản phẩm hiện chưa có khu vực riêng đọc trực tiếp trường này; nên đưa các ý quan trọng vào **Mô tả ngắn** hoặc **Thông số kỹ thuật**. |

Ví dụ **Mô tả ngắn**:

```text
- Phạm vi đo: -20 đến 70 °C; 0 đến 100 %RH
- Độ chính xác: ±2 %RH; ±0,5 °C
- Số kênh đo: 10 kênh
```

Ví dụ **Tính năng nổi bật**:

```text
Chuẩn bảo vệ IP67
Giao tiếp RS485 Modbus RTU
Nguồn cấp 24 VDC
```

#### F. Thông số vật lý

| Trường | Đơn vị |
|---|---|
| **Khối lượng** | kg |
| **Chiều dài** | mm |
| **Chiều rộng** | mm |
| **Chiều cao** | mm |

Các trường này được lưu để quản lý dữ liệu sản phẩm. Giao diện chi tiết hiện tại chưa có khu vực riêng hiển thị chúng; nếu khách hàng cần thấy ngay, hãy nhập thêm trong bảng **Thông số kỹ thuật**.

#### G. Các lựa chọn xuất bản

| Trường | Tác dụng |
|---|---|
| **Đánh dấu Mới** | Hiển thị nhãn **Mới** trên thẻ và trang sản phẩm. |
| **Đánh dấu Bán chạy** | Lưu cờ bán chạy để dùng cho sắp xếp/khu vực giới thiệu. |
| **Nổi bật** | Cho phép sản phẩm xuất hiện trong nhóm sản phẩm nổi bật trên trang chủ. |
| **Bắt buộc báo giá** | Ghi đè hành vi mua trực tiếp và chuyển sản phẩm sang luồng báo giá. Chỉ bật khi thật sự cần. |
| **Sort order** | Số nhỏ ưu tiên trước trong các truy vấn có sắp xếp theo thứ tự. |

#### H. SEO

| Trường | Khuyến nghị |
|---|---|
| **Meta title** | Tối đa khoảng 70 ký tự. |
| **Meta description** | Tối đa khoảng 160 ký tự. |
| **Meta keywords** | Các từ khóa cách nhau bằng dấu phẩy. |
| **Canonical URL** | Chỉ nhập khi cần chỉ định URL chuẩn khác. |
| **OG image** | Khuyến nghị `1200 × 630 px`. |

Các trường SEO được lưu trong hệ thống. Ở trang chi tiết sản phẩm hiện tại, tiêu đề và mô tả trình duyệt vẫn ưu tiên **Tên sản phẩm** và **Mô tả ngắn**; vì vậy hai trường này phải luôn được viết tốt.

### 5.2. Thư viện ảnh sản phẩm

Nằm phía dưới biểu mẫu sản phẩm, mục **Ảnh sản phẩm**.

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Ảnh** | Tải ảnh góc nhìn hoặc chi tiết sản phẩm. | Tạo thư viện ảnh nhỏ bên dưới ảnh chính. Ảnh đầu tiên được dùng làm ảnh lớn ban đầu trên trang chi tiết. |
| **Alt text** | Mô tả ngắn nội dung ảnh, ví dụ `Mặt trước bộ điều khiển GTC-AIR-01`. | Hỗ trợ SEO và khả năng tiếp cận. |
| **Ảnh chính** | Chỉ chọn một ảnh. | Hệ thống tự bỏ cờ ảnh chính ở ảnh khác của cùng sản phẩm. |
| **Sort order** | `10, 20, 30...` | Sắp xếp ảnh trong thư viện. |

Nếu đã thêm thư viện ảnh, trang chi tiết ưu tiên ảnh trong thư viện trước ảnh đại diện.

### 5.3. Thông số kỹ thuật

Nằm phía dưới biểu mẫu sản phẩm, mục **Thông số kỹ thuật**.

| Trường | Ví dụ | Tác dụng |
|---|---|---|
| **Nhóm thông số** | `Thông số điện` | Tạo tiêu đề nhóm trong tab **Thông số kỹ thuật**. Các dòng cùng tên nhóm được gom chung. |
| **Tên thông số** | `Nguồn cấp` | Cột bên trái của bảng. |
| **Giá trị** | `220 VAC / 50 Hz` | Cột bên phải của bảng. |
| **Đơn vị** | `V`, `A`, `mm`, `°C` | Hiển thị sau giá trị. Để trống nếu giá trị đã chứa đầy đủ đơn vị. |
| **Sort order** | `10`, `20`, `30` | Sắp xếp từng dòng. |

Không nhập lặp đơn vị. Ví dụ, nếu **Giá trị** đã là `220 VAC`, hãy để trống **Đơn vị**.

### 5.4. Tài liệu sản phẩm

Nằm phía dưới biểu mẫu sản phẩm, mục **Tài liệu sản phẩm**.

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Tiêu đề** | Ví dụ `Hướng dẫn lắp đặt và vận hành`. | Tên khách hàng nhìn thấy trong tab **Tài liệu**. |
| **Loại tài liệu** | Chọn Datasheet, Hướng dẫn sử dụng, Chứng nhận, Bản vẽ, Phần mềm/Driver hoặc Khác. | Phân loại tài liệu. |
| **File** | Tải PDF hoặc tệp phù hợp. | Khách hàng bấm để xem hoặc tải xuống. |
| **Sort order** | Số nhỏ đứng trước. | Sắp xếp danh sách tài liệu. |

Tên tệp khuyến nghị:

```text
huong-dan-su-dung-gtc-air-01-v1.0.pdf
datasheet-gtc-air-01.pdf
so-do-dau-noi-gtc-air-01.pdf
```

### 5.5. Sản phẩm liên quan

| Trường | Tác dụng |
|---|---|
| **Sản phẩm liên quan** | Chọn sản phẩm đã có trong hệ thống. |
| **Loại liên kết** | Phụ kiện, sản phẩm thay thế, tương thích hoặc bán kèm. |
| **Sort order** | Sắp xếp danh sách. |

Chức năng quản trị đã lưu đầy đủ quan hệ sản phẩm. Tuy nhiên trang chi tiết sản phẩm hiện đang dùng tên biến hiển thị chưa đồng nhất với dữ liệu từ view, vì vậy cần kiểm tra ngoài website sau khi gắn; nếu khu vực **Sản phẩm liên quan** không xuất hiện thì đây là vấn đề giao diện, không phải do nhập sai.

### 5.6. Kiểm tra trước khi xuất bản sản phẩm

- [ ] Tên, SKU và slug đúng; SKU không trùng.
- [ ] Đã chọn danh mục và thương hiệu.
- [ ] Có ảnh đại diện và alt text cho ảnh thư viện.
- [ ] Loại giá khớp với dữ liệu giá.
- [ ] Giá khuyến mãi nhỏ hơn giá niêm yết.
- [ ] Tình trạng kho khớp số lượng tồn.
- [ ] Mô tả ngắn không quá 500 ký tự.
- [ ] Mô tả chi tiết được chia đoạn và dùng danh sách chuẩn.
- [ ] Thông số kỹ thuật đã chia nhóm.
- [ ] Tệp tài liệu mở được.
- [ ] Chuyển trạng thái sang **Published** sau cùng.

## 6. Nhóm “Giải pháp”

### 6.1. Danh mục giải pháp

Đường dẫn admin: **Giải pháp → Danh mục giải pháp**.

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Name** | Ví dụ `Quan trắc môi trường`. | Hiển thị trong bộ lọc và nhãn danh mục giải pháp. |
| **Slug** | Ví dụ `quan-trac-moi-truong`. | Tạo URL lọc `/solutions/category/quan-trac-moi-truong/`. |
| **Description** | Giới thiệu ngắn. | Được lưu cho danh mục; danh sách hiện chủ yếu hiển thị tên. |
| **Icon class** | Lớp CSS biểu tượng. | Trường nâng cao, có thể để trống. |
| **Thumbnail** | Ảnh đại diện danh mục. | Được lưu để mở rộng giao diện; trang danh sách hiện chưa dùng trực tiếp. |
| **Is active** | Đánh dấu khi đang sử dụng. | Chỉ danh mục hoạt động xuất hiện trong điều hướng/bộ lọc giải pháp. |
| **Sort order** | Số nhỏ đứng trước. | Sắp xếp bộ lọc danh mục. |

### 6.2. Tạo hoặc sửa giải pháp

Đường dẫn admin: **Giải pháp → Giải pháp**.

#### A. Thông tin cơ bản

| Trường | Cách nhập | Vị trí hiển thị |
|---|---|---|
| **Title** | Tên chính của giải pháp. | Tiêu đề trang chủ, thẻ giải pháp, trang danh sách và trang chi tiết. |
| **Subtitle** | Một câu phụ ngắn. | Hiển thị bên dưới tiêu đề tại thẻ và phần đầu trang chi tiết. |
| **Slug** | Để tự sinh rồi kiểm tra. | Tạo URL `/solutions/<slug>/`. |
| **Solution category** | Chọn danh mục giải pháp. | Tạo nhãn danh mục và bộ lọc. |

#### B. Hình ảnh và video

| Trường | Cách nhập | Vị trí hiển thị |
|---|---|---|
| **Thumbnail** | Ảnh ngang, khuyến nghị `1200 × 675 px`. | Bắt buộc; hiển thị trên trang chủ và danh sách giải pháp, đồng thời làm ảnh dự phòng cho phần đầu trang chi tiết. |
| **Hero image** | Ảnh ngang chất lượng tốt. | Ảnh nền/phần đầu trang chi tiết; nếu trống sẽ dùng thumbnail. |
| **Hero video URL** | Dán URL YouTube hoặc Vimeo hợp lệ. | Hiển thị video nhúng trên trang chi tiết. Hệ thống tự chuyển URL xem thông thường sang URL nhúng. Các nguồn khác sẽ bị từ chối. |

Ví dụ URL hợp lệ:

```text
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://vimeo.com/123456789
```

#### C. Nội dung chính

| Trường | Cách nhập | Vị trí hiển thị |
|---|---|---|
| **Short description** | Một đoạn tóm tắt không quá 500 ký tự. | Thẻ giải pháp và phần giới thiệu đầu trang chi tiết. |
| **Overview** | Nội dung đầy đủ bằng CKEditor. | Phần **Tổng quan / Về giải pháp này** trên trang chi tiết. |

Với danh sách tính năng trong Overview, hãy dùng nút tạo danh sách của CKEditor. Không gõ dấu `+` rồi chèn dòng trống giữa từng ý.

#### D. Triển khai thực tế

| Trường | Ví dụ | Vị trí hiển thị |
|---|---|---|
| **Đơn vị / địa điểm triển khai** | `Nhà máy ABC` | Tên nổi bật trong khối **Triển khai thực tế**. |
| **Địa chỉ triển khai** | `KCN Quế Võ, Bắc Ninh` | Hiển thị bên dưới tên đơn vị. |
| **Thời gian triển khai** | Chọn một ngày đại diện. | Website hiển thị theo tháng/năm. |

Khối triển khai chỉ xuất hiện khi có ít nhất một trường trên hoặc có ảnh triển khai.

#### E. Vấn đề khách hàng

Mỗi dòng là một vấn đề, các thành phần cách nhau bằng dấu `|`:

```text
Tiêu đề | Mô tả | icon
```

Ví dụ:

```text
Khó giám sát từ xa | Không có dữ liệu theo thời gian thực | eye-off
Tốn nhân lực ghi chép | Nhân viên phải tổng hợp số liệu thủ công | users
Không cảnh báo kịp thời | Sự cố chỉ được phát hiện sau khi vượt ngưỡng | alert-triangle
```

Kết quả hiển thị:

- Mỗi dòng tạo một mục trong cột **Thách thức – Vấn đề gặp phải**.
- **Tiêu đề** hiển thị chữ đậm.
- **Mô tả** hiển thị bên dưới.
- Giao diện hiện dùng cùng một biểu tượng cảnh báo cố định cho mọi vấn đề; phần `icon` vẫn được lưu nhưng hiện chưa làm thay đổi biểu tượng ngoài trang.

Không nhập dạng Python hoặc JSON như `{'title': '...'}`. Biểu mẫu admin sẽ tự chuyển từng dòng thành dữ liệu đúng định dạng.

#### F. Lợi ích

Mỗi dòng có định dạng:

```text
Tiêu đề | Chỉ số nổi bật | Mô tả | icon
```

Ví dụ:

```text
Giảm chi phí vận hành | 30% | Tối ưu điện năng và nhân lực | trending-down
Theo dõi liên tục | 24/7 | Xem dữ liệu từ xa theo thời gian thực | activity
Rút ngắn thời gian xử lý | 50% | Cảnh báo ngay khi vượt ngưỡng | clock
```

Kết quả hiển thị:

- **Chỉ số nổi bật** như `30%` được hiển thị lớn.
- **Tiêu đề** hiển thị cạnh chỉ số.
- **Mô tả** hiển thị phía dưới.
- Giao diện hiện dùng biểu tượng dấu kiểm cố định; giá trị `icon` được lưu nhưng chưa thay đổi biểu tượng công khai.

#### G. Quy trình hoạt động

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Workflow title** | Ví dụ `Quy trình giám sát và cảnh báo`. | Tiêu đề của khu vực quy trình. Nếu để trống, website dùng `Quy trình hoạt động`. |
| **Workflow description** | Một đoạn mô tả ngắn. | Hiển thị bên dưới tiêu đề quy trình. |

Các bước cụ thể được nhập tại phần **Các bước quy trình** phía dưới biểu mẫu.

#### H. Kêu gọi hành động (CTA)

| Trường | Tác dụng |
|---|---|
| **CTA title** | Tiêu đề lớn ở khối kêu gọi hành động cuối trang. |
| **CTA primary text** | Chữ trên nút chính. |
| **CTA primary URL** | Đường dẫn của nút chính. |
| **CTA secondary text** | Chữ trên nút phụ. |
| **CTA secondary URL** | Đường dẫn của nút phụ. |

Nếu để trống URL, website tự dùng các nút mặc định:

- Nút chính: **Đặt lịch demo** → `/contact/demo/`.
- Nút phụ: **Yêu cầu báo giá** → `/orders/quote/`.

Quan trọng: chữ CTA tùy chỉnh chỉ được dùng khi URL tương ứng cũng có giá trị. Nếu chỉ nhập chữ nhưng để trống URL, giao diện vẫn dùng nút mặc định.

Ví dụ CTA tùy chỉnh:

```text
CTA title: Trao đổi với kỹ sư của chúng tôi
CTA primary text: Đặt lịch khảo sát
CTA primary URL: /contact/demo/
CTA secondary text: Nhận báo giá
CTA secondary URL: /orders/quote/
```

#### I. Xuất bản

| Trường | Tác dụng |
|---|---|
| **Status** | Chỉ giải pháp Published mới xuất hiện công khai. |
| **Published at** | Thời điểm xuất bản. |
| **Is featured** | Đưa giải pháp vào khu vực nổi bật trên trang chủ và ưu tiên ở danh sách. |
| **Sort order** | Số nhỏ ưu tiên trước. |

### 6.3. Thư viện ảnh triển khai thực tế

Nằm phía dưới biểu mẫu giải pháp, mục **Thư viện ảnh triển khai thực tế**.

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Ảnh triển khai** | Ảnh chụp tại địa điểm thực tế. | Hiển thị trong khối triển khai và mở được thư viện ảnh lớn. |
| **Chú thích** | Ví dụ `Tủ điều khiển sau khi hoàn thiện`. | Chú thích dưới ảnh và trong trình xem ảnh. |
| **Mô tả ảnh (SEO)** | Mô tả đúng nội dung ảnh. | Dùng cho alt text và khả năng tiếp cận. |
| **Ảnh chính** | Chọn một ảnh đại diện. | Ảnh này được ưu tiên đứng đầu; chọn ảnh mới sẽ tự bỏ chọn ảnh chính cũ. |
| **Sort order** | `10, 20, 30...` | Sắp xếp các ảnh còn lại. |

Website hiển thị trước tối đa ba ô ảnh; nếu có nhiều hơn sẽ hiện số lượng ảnh còn lại và người dùng có thể mở toàn bộ thư viện.

### 6.4. Sản phẩm trong giải pháp

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Product** | Chọn một sản phẩm đã Published. | Gắn sản phẩm vào giải pháp. |
| **Is featured** | Đánh dấu cho sản phẩm chính. | Sản phẩm xuất hiện ngay trong nhóm nổi bật của giải pháp. |
| **Role description** | Ví dụ `Bộ điều khiển trung tâm`. | Hiển thị vai trò ngắn trên thẻ sản phẩm. |
| **Sort order** | Số nhỏ đứng trước. | Sắp xếp sản phẩm trong giải pháp. |

Phải đánh dấu ít nhất một sản phẩm là **Is featured** nếu muốn khu vực sản phẩm xuất hiện. Khi đã có sản phẩm nổi bật, nút **Xem tất cả** có thể mở các sản phẩm còn lại.

### 6.5. Các khối kiến trúc

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Title** | Ví dụ `Lớp cảm biến`. | Tiêu đề thẻ trong phần **Kiến trúc hệ thống – Cách hoạt động**. |
| **Description** | Mô tả nhiệm vụ của khối. | Hiển thị dưới tiêu đề. |
| **Image** | Sơ đồ hoặc ảnh minh họa, ưu tiên tỷ lệ `4:3`. | Hiển thị ở đầu thẻ. |
| **Sort order** | Số nhỏ đứng trước. | Sắp xếp các khối. |

### 6.6. Các bước quy trình

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Step number** | `1`, `2`, `3`... | Xác định thứ tự bước và hiển thị số nếu không có icon/ảnh. |
| **Title** | Tên ngắn của bước. | Tiêu đề bước. |
| **Description** | Mô tả một hoặc hai câu. | Nội dung dưới tiêu đề. |
| **Icon class** | Lớp icon CSS hợp lệ. | Nếu có, website ưu tiên hiển thị icon. Chỉ dùng khi biết chính xác thư viện icon đang hỗ trợ. |
| **Image** | Ảnh biểu tượng nhỏ. | Chỉ được dùng khi **Icon class** để trống. |

Thứ tự ưu tiên hiển thị trong vòng tròn: **Icon class → Image → Step number**. Cách an toàn nhất là để trống icon và ảnh để website hiển thị số bước.

### 6.7. Dự án khách hàng

Đường dẫn admin: **Giải pháp → Dự án khách hàng**.

Mỗi dự án khách hàng là một case study gắn với một giải pháp.

| Trường | Cách nhập | Tác dụng và vị trí hiển thị |
|---|---|---|
| **Solution** | Chọn giải pháp tương ứng. | Dự án xuất hiện trên trang chi tiết giải pháp đó. |
| **Company name** | Tên đơn vị khách hàng. | Hiển thị trên thẻ dự án. |
| **Slug** | Tự sinh từ tên công ty. | Lưu định danh cho dự án. Hiện chưa có trang chi tiết case riêng. |
| **Company logo** | Logo rõ, nền trong suốt nếu có thể. | Hiển thị trên thẻ dự án. |
| **Industry** | Ví dụ `Sản xuất thực phẩm`. | Hiển thị cạnh quốc gia. |
| **Country** | Mặc định `Việt Nam`. | Hiển thị trên thẻ dự án. |
| **Challenge** | Mô tả vấn đề ban đầu. | Được lưu trong hệ thống; thẻ dự án hiện chưa hiển thị đoạn này. |
| **Solution applied** | Mô tả giải pháp đã áp dụng. | Được lưu trong hệ thống; thẻ dự án hiện chưa hiển thị đoạn này. |
| **Testimonial** | Trích dẫn ngắn của khách hàng. | Hiển thị trên thẻ dự án, tối đa khoảng ba dòng. |
| **Testimonial author** | Họ tên người phát biểu. | Hiển thị dưới trích dẫn. |
| **Testimonial title** | Chức danh người phát biểu. | Hiển thị dưới tên. |
| **Status** | Chọn Published khi được phép công khai. | Chỉ dự án Published mới được hiển thị. |

Trường **Kết quả đạt được** nhập mỗi kết quả trên một dòng:

```text
Chỉ số | Giá trị | Đơn vị
```

Ví dụ:

```text
Tiết kiệm nước | 30 | %
Giảm thời gian kiểm tra | 50 | %
Điểm giám sát | 24 | điểm
```

Trang giải pháp hiện hiển thị tối đa ba kết quả đầu tiên trên mỗi thẻ dự án.

### 6.8. Kiểm tra trước khi xuất bản giải pháp

- [ ] Tiêu đề, slug, danh mục và thumbnail đầy đủ.
- [ ] Mô tả ngắn rõ ràng, không quá 500 ký tự.
- [ ] Overview dùng tiêu đề và danh sách chuẩn.
- [ ] Video là liên kết YouTube/Vimeo hợp lệ.
- [ ] Vấn đề và lợi ích dùng đúng dấu `|`, mỗi mục một dòng.
- [ ] Thông tin triển khai và ảnh thực tế đúng dự án.
- [ ] Có alt text và chú thích ảnh.
- [ ] Có ít nhất một sản phẩm nổi bật nếu muốn hiển thị sản phẩm.
- [ ] Các bước quy trình không trùng số.
- [ ] CTA dẫn tới đúng trang.
- [ ] Chỉ chuyển sang Published sau khi xem thử ngoài website.

## 7. Nhóm “Bài viết”

### 7.1. Danh mục bài viết

Đường dẫn admin: **Bài viết → Danh mục bài viết**.

| Trường | Cách nhập | Tác dụng |
|---|---|---|
| **Name** | Ví dụ `Kiến thức IoT`. | Hiển thị trong bộ lọc, breadcrumb và trang danh mục bài viết. |
| **Slug** | Ví dụ `kien-thuc-iot`. | Tạo URL `/blog/category/kien-thuc-iot/`. |
| **Description** | Một hoặc hai câu. | Hiển thị tại đầu trang danh mục bài viết. |
| **Is active** | Đánh dấu khi đang sử dụng. | Dùng để kiểm soát danh mục hoạt động. |
| **Sort order** | Số nhỏ đứng trước. | Sắp xếp danh mục. |

### 7.2. Tạo hoặc sửa bài viết

| Trường | Cách nhập | Tác dụng và vị trí hiển thị |
|---|---|---|
| **Title** | Tiêu đề rõ nội dung, không viết toàn bộ bằng chữ hoa. | Tiêu đề thẻ, trang chi tiết và kết quả tìm kiếm. |
| **Slug** | Để tự sinh rồi kiểm tra. | Tạo URL `/blog/<slug>/`. |
| **Post type** | Bài viết kỹ thuật, Tin tức, Case Study hoặc Hướng dẫn. | Hiển thị thành nhãn loại bài và hỗ trợ lọc. |
| **Category** | Chọn danh mục bài viết. | Hiển thị nhãn và breadcrumb. |
| **Author** | Chọn tài khoản người viết. | Hiển thị tên, chức danh và công ty của tác giả nếu có. |
| **Thumbnail** | Ảnh ngang `16:9`, khuyến nghị `1200 × 675 px`. | Ảnh nền phần đầu, ảnh chính bài viết, thẻ trang chủ và danh sách. |
| **Short description** | Tóm tắt không quá 500 ký tự. | Hiển thị dưới tiêu đề và trên thẻ bài viết; dùng làm mô tả SEO mặc định. |
| **Content** | Soạn bằng CKEditor. | Toàn bộ nội dung bài viết. |
| **Read time** | Số phút, ví dụ `5`. | Hiển thị `5 phút đọc`. |
| **Tags** | Phân cách bằng dấu phẩy. | Hiển thị thành liên kết tìm kiếm ở cuối bài và sidebar. |
| **Related products** | Chọn các sản phẩm liên quan. | Hiển thị thẻ sản phẩm dưới nội dung. |
| **Related solutions** | Chọn các giải pháp liên quan. | Hiển thị danh sách giải pháp dưới nội dung. |
| **Meta title** | Tối đa khoảng 70 ký tự. | Dữ liệu SEO. |
| **Meta description** | Tối đa khoảng 160 ký tự. | Dữ liệu SEO. |
| **Status** | Chọn Published khi bài hoàn chỉnh. | Chỉ bài Published được hiển thị. |
| **Published at** | Ngày giờ xuất bản. | Hiển thị trên bài và dùng để sắp xếp bài mới. |
| **Is featured** | Đánh dấu bài quan trọng. | Dùng cho khu vực bài nổi bật. |
| **Sort order** | Thứ tự ưu tiên khi truy vấn hỗ trợ. | Số nhỏ ưu tiên trước. |

Ví dụ tags đúng:

```text
IoT, Cảm biến, Quan trắc môi trường, RS485
```

Không nhập:

```text
#IoT #Cảm biến #RS485
```

### 7.3. Bố cục nội dung bài viết được khuyến nghị

```text
Đoạn mở đầu: vấn đề bài viết giải quyết

Tiêu đề cấp 2: Bối cảnh hoặc khái niệm
Đoạn giải thích

Tiêu đề cấp 2: Hướng dẫn thực hiện
1. Bước thứ nhất
2. Bước thứ hai
3. Bước thứ ba

Tiêu đề cấp 2: Lưu ý
Danh sách các cảnh báo hoặc kinh nghiệm

Tiêu đề cấp 2: Kết luận
Tóm tắt và lời kêu gọi liên hệ
```

### 7.4. Kiểm tra trước khi xuất bản bài viết

- [ ] Tiêu đề, slug, loại bài và danh mục đúng.
- [ ] Có tác giả và thumbnail.
- [ ] Mô tả ngắn không quá 500 ký tự.
- [ ] Nội dung có tiêu đề cấp 2, đoạn văn và danh sách rõ ràng.
- [ ] Ảnh trong bài có mô tả thay thế nếu trình soạn thảo hỗ trợ.
- [ ] Thời gian đọc hợp lý.
- [ ] Tags cách nhau bằng dấu phẩy.
- [ ] Sản phẩm và giải pháp liên quan đúng nội dung.
- [ ] Có ngày xuất bản và trạng thái Published.

## 8. Nhóm “Đơn hàng và báo giá”

Các mục trong nhóm này chủ yếu do khách hàng tạo từ website. Người quản trị nên **xử lý bản ghi có sẵn**, không tạo thủ công nếu không có quy trình nghiệp vụ riêng.

### 8.1. Đơn hàng

Đường dẫn admin: **Đơn hàng và báo giá → Đơn hàng**.

#### Các trường cần hiểu

| Nhóm | Trường | Tác dụng |
|---|---|---|
| Thông tin đơn | **Order number** | Mã tự sinh. `PO-...` là đơn mua; `QT-...` là yêu cầu báo giá đi qua giỏ. |
| Thông tin đơn | **Order type** | Phân biệt đơn mua hàng và yêu cầu báo giá. |
| Thông tin đơn | **Status** | Theo dõi tiến độ xử lý. |
| Khách hàng | Email, họ tên, công ty, điện thoại | Bản chụp thông tin tại thời điểm đặt hàng. |
| Địa chỉ | Shipping/Billing address | Dữ liệu JSON của địa chỉ giao hàng và thanh toán. Không chỉnh nếu không cần thiết. |
| Tài chính | Subtotal/Total | Hệ thống tính; dòng chờ báo giá không bị coi là miễn phí. |
| Ghi chú | Customer notes | Nội dung khách hàng gửi. |
| Ghi chú | Internal notes | Ghi chú nội bộ, không hiển thị cho khách hàng. |
| Vận chuyển | Tracking number | Mã vận đơn. |
| Vận chuyển | Shipped at/Delivered at | Thời điểm giao vận và hoàn tất. |

Quy trình trạng thái đề xuất:

```text
Chờ xử lý → Đã xác nhận → Đang xử lý → Đã giao vận → Đã giao hàng
```

Các trạng thái khác:

- **Đã hủy**: đơn không tiếp tục xử lý.
- **Đã hoàn tiền**: đã hoàn lại tiền theo quy trình kế toán.

Có thể chọn nhiều đơn ở danh sách, chọn thao tác rồi nhấn **Thực hiện**:

- **Xác nhận đơn hàng**: chỉ áp dụng cho đơn Chờ xử lý.
- **Chuyển sang Đang xử lý**: chỉ áp dụng cho đơn Đã xác nhận.
- **Đánh dấu Đã giao vận**: chỉ áp dụng cho đơn Đang xử lý và tự ghi thời gian giao vận.
- **Hủy đơn hàng**: áp dụng cho đơn Chờ xử lý hoặc Đã xác nhận.

#### Các dòng đơn hàng

- **Product SKU** và **Product name** là bản chụp tại thời điểm đặt; đổi tên sản phẩm sau này không làm mất lịch sử.
- **Pricing type** là loại giá tại thời điểm đặt.
- Nếu giá chưa xác định, thành tiền hiển thị **Chờ báo giá**, không hiển thị `0 ₫`.
- Không sửa đơn giá hoặc số lượng nếu chưa có xác nhận nghiệp vụ.

Khi khách đặt đơn thành công, hệ thống gửi email xác nhận cho khách và thông báo cho email công ty nếu cấu hình email và Celery worker đang hoạt động. Việc đổi trạng thái trong admin hiện không tự gửi email cập nhật trạng thái cho khách.

### 8.2. Yêu cầu báo giá

Đường dẫn admin: **Đơn hàng và báo giá → Yêu cầu báo giá**.

| Trường | Tác dụng |
|---|---|
| **Reference** | Mã RFQ tự sinh, ví dụ `RFQ-202608-12345`. |
| **Status** | Trạng thái xử lý yêu cầu. |
| **Solution** | Giải pháp khách đang quan tâm. |
| **Application** | Ứng dụng hoặc ngành hàng cụ thể. |
| **Name, email, phone, company** | Thông tin liên hệ của người gửi. |
| **Message** | Nhu cầu chi tiết của khách hàng. |
| **Assigned to** | Nhân viên phụ trách; có thể chọn nhanh ngay ở danh sách. |
| **Internal notes** | Ghi chú nội bộ. Không gửi cho khách. |
| **Converted order link** | Liên kết tới đơn hàng đã được tạo từ báo giá, nếu có. |

Quy trình đề xuất:

```text
Mới → Đang xem xét → Đã báo giá → Đã chấp nhận
                                  └→ Từ chối
```

Các thao tác hàng loạt:

- **Chuyển sang Đang xem xét**: chỉ áp dụng cho yêu cầu Mới.
- **Đánh dấu Đã báo giá**: chỉ áp dụng cho yêu cầu Đang xem xét.
- **Từ chối báo giá**: áp dụng cho Mới hoặc Đang xem xét.

Các dòng báo giá cho biết sản phẩm, SKU, tên sản phẩm, số lượng và ghi chú riêng.

Khi khách gửi biểu mẫu báo giá, hệ thống gửi email xác nhận đã tiếp nhận cho khách và email thông báo cho công ty nếu cấu hình email/Celery hoạt động. Nút **Đánh dấu Đã báo giá** trong admin hiện chỉ đổi trạng thái; nó không tự tạo file báo giá và không tự gửi báo giá chính thức. Nhân viên vẫn phải lập và gửi báo giá qua quy trình của công ty.

## 9. Nhóm “Liên hệ và đăng ký demo”

### 9.1. Yêu cầu liên hệ

Mục này chỉ nhận dữ liệu từ biểu mẫu công khai; admin không cho tạo thủ công.

| Trường | Ý nghĩa |
|---|---|
| **Người gửi** | Họ tên, email, điện thoại, công ty và quốc gia. |
| **Inquiry type** | Tư vấn chung, hỗ trợ kỹ thuật, kinh doanh/báo giá, hỗ trợ sau bán hàng hoặc hợp tác. |
| **Subject** | Tiêu đề yêu cầu. |
| **Message** | Nội dung khách gửi. |
| **Status** | Mới, Đã đọc, Đã trả lời hoặc Đã đóng. |
| **Internal notes** | Ghi chú nội bộ, không hiển thị cho khách. |
| **Metadata** | IP, trình duyệt, trang nguồn và thời gian; chỉ dùng kiểm tra kỹ thuật/chống spam. |

Quy trình đề xuất:

```text
Mới → Đã đọc → Đã trả lời → Đã đóng
```

Các thao tác **Đánh dấu Đã đọc**, **Đã trả lời** và **Đóng liên hệ** chỉ thay đổi trạng thái; không tự gửi thư trả lời khách hàng.

Khi biểu mẫu mới được gửi, hệ thống gửi thông báo tới email công ty nếu cấu hình email/Celery hoạt động.

### 9.2. Yêu cầu đăng ký demo

Mục này được tạo từ biểu mẫu `/contact/demo/`.

| Trường | Ý nghĩa |
|---|---|
| **Người đăng ký** | Tên, email, điện thoại, công ty, chức danh và quốc gia. |
| **Solution** | Giải pháp khách muốn xem demo. |
| **Preferred date** | Ngày khách mong muốn. Đây chưa phải ngày đã được công ty xác nhận. |
| **Message** | Ghi chú của khách. |
| **Status** | Mới, Đã lên lịch, Hoàn thành hoặc Đã hủy. |

Quy trình đề xuất:

```text
Mới → liên hệ xác nhận lịch → Đã lên lịch → Hoàn thành
                                └→ Đã hủy
```

Thay đổi trạng thái trong admin không tự gửi lịch hẹn cho khách. Người phụ trách cần liên hệ qua email hoặc điện thoại.

## 10. Nhóm “Khách hàng”

### 10.1. Tài khoản khách hàng

Tài khoản thường được tạo khi khách đăng ký. Admin cũng có thể tạo tài khoản mới khi cần.

| Trường | Cách sử dụng |
|---|---|
| **Email** | Tên đăng nhập và phải là duy nhất. |
| **Password** | Mật khẩu được mã hóa. Khi đổi mật khẩu, dùng liên kết/form đổi mật khẩu; không sửa chuỗi mã hóa trực tiếp. |
| **First name / Last name / Phone** | Thông tin cá nhân. |
| **Company name** | Tên công ty. |
| **Company type** | Nhà sản xuất, System Integrator, Nhà phân phối, End User hoặc Khác. |
| **Job title** | Chức danh; có thể hiển thị trong thẻ tác giả bài viết. |
| **Industry** | Ngành hoạt động. |
| **Is active** | Cho phép tài khoản đăng nhập. Bỏ chọn để khóa tài khoản mà không xóa dữ liệu. |
| **Is verified** | Đánh dấu tài khoản đã được xác minh theo quy trình nội bộ. |
| **Is VIP** | Nhãn khách hàng ưu tiên để quản lý nội bộ. |
| **Newsletter subscribed** | Khách đồng ý nhận bản tin. Không tự đồng nghĩa với việc hệ thống đang gửi newsletter. |
| **Is staff** | Cho phép truy cập trang admin nếu đồng thời có quyền phù hợp. Chỉ cấp cho nhân viên. |
| **Is superuser** | Có toàn bộ quyền. Chỉ cấp cho quản trị viên kỹ thuật đáng tin cậy. |
| **Groups / User permissions** | Phân quyền chi tiết trong admin. |

Không cấp **Is staff** hoặc **Is superuser** cho khách hàng thông thường.

### 10.2. Địa chỉ khách hàng

Địa chỉ được nhập ngay phía dưới tài khoản khách hàng.

| Trường | Ý nghĩa |
|---|---|
| **Label** | Tên gợi nhớ, ví dụ `Văn phòng`, `Kho Hà Nội`. |
| **Address line 1** | Địa chỉ chính. |
| **City / Country** | Tỉnh, thành phố và quốc gia. |
| **Default shipping** | Địa chỉ giao hàng mặc định. |
| **Default billing** | Địa chỉ thanh toán mặc định. |

Chỉ nên có một địa chỉ giao hàng mặc định và một địa chỉ thanh toán mặc định cho mỗi khách hàng.

## 11. Nhóm “Giỏ hàng”

Giỏ hàng được hệ thống tự tạo khi khách thêm sản phẩm. Admin không cho tạo giỏ thủ công.

Mục này chủ yếu dùng để kiểm tra:

- Giỏ thuộc khách đăng nhập hay phiên khách vãng lai.
- Giỏ còn hoạt động hay đã hoàn tất.
- Các sản phẩm, số lượng và loại giá đã thêm.
- Giá tạm tính hoặc trạng thái **Chờ báo giá**.

Không nên sửa giỏ hàng của khách trong admin trừ khi đang xử lý sự cố kỹ thuật. Không xóa giỏ đang hoạt động khi khách có thể vẫn đang thao tác.

## 12. Phân quyền đề xuất cho người dùng admin

| Vai trò | Quyền đề xuất |
|---|---|
| **Biên tập nội dung** | Xem/thêm/sửa danh mục, sản phẩm, giải pháp và bài viết; không có quyền xóa hàng loạt hoặc quản lý tài khoản. |
| **Kinh doanh** | Xem/sửa yêu cầu báo giá, liên hệ, demo và đơn hàng; chỉ xem sản phẩm. |
| **Quản lý nội dung** | Toàn quyền nội dung, được xuất bản và lưu trữ; không phải superuser. |
| **Quản trị kỹ thuật** | Quản lý người dùng, phân quyền và cấu hình; có thể là superuser. |

Nên tạo **Groups** theo vai trò rồi gán quyền cho nhóm, thay vì cấp từng quyền riêng lẻ cho từng người.

## 13. Những trường cần lưu ý theo giao diện hiện tại

Đây là các trường đã có trong cơ sở dữ liệu/admin nhưng giao diện công khai hiện chưa sử dụng đầy đủ:

| Trường/chức năng | Trạng thái hiện tại |
|---|---|
| Tính năng nổi bật của sản phẩm | Được lưu nhưng chưa có khu vực hiển thị riêng. |
| Khối lượng và kích thước sản phẩm | Được lưu nhưng chưa hiển thị riêng; nên nhập lại ở Thông số kỹ thuật nếu khách cần xem. |
| Sản phẩm liên quan ở trang sản phẩm | Admin lưu được, nhưng tên biến giữa view và template hiện chưa đồng nhất; cần kiểm tra sau khi nhập. |
| Icon của Vấn đề và Lợi ích | Được lưu nhưng giao diện hiện dùng icon cố định. |
| Challenge và Solution applied của Dự án khách hàng | Được lưu nhưng thẻ dự án hiện chưa hiển thị. |
| Mô tả/thumbnail/icon của Danh mục giải pháp | Được lưu; danh sách hiện chủ yếu dùng tên, slug, trạng thái và thứ tự. |
| Một số trường SEO chi tiết | Được lưu, nhưng trang chi tiết hiện vẫn ưu tiên tên/tiêu đề và mô tả ngắn. |
| Đổi trạng thái đơn, báo giá, liên hệ, demo | Chỉ cập nhật dữ liệu; không tự gửi email trạng thái cho khách. |

Các ghi chú này giúp phân biệt giữa **nhập sai dữ liệu** và **giao diện chưa sử dụng trường dữ liệu**.

## 14. Quy trình kiểm duyệt nội dung đề xuất

1. Người nhập tạo nội dung ở trạng thái **Draft**.
2. Kiểm tra chính tả, ảnh, giá, liên kết và tài liệu.
3. Dùng **Lưu và tiếp tục chỉnh sửa**.
4. Người duyệt mở trang admin để kiểm tra lần cuối.
5. Chuyển trạng thái thành **Published**, nhập thời gian xuất bản nếu cần.
6. Mở trang công khai bằng cửa sổ riêng tư.
7. Kiểm tra cả máy tính và điện thoại.
8. Nếu nội dung không còn sử dụng, chuyển sang **Archived** thay vì xóa ngay.

## 15. Checklist kiểm tra nhanh sau khi nhập liệu

- [ ] Nội dung đã ở đúng danh mục.
- [ ] Slug ngắn, không dấu và không trùng.
- [ ] Không còn đoạn nội dung thử nghiệm.
- [ ] Ảnh đúng chiều, không bị mờ hoặc cắt mất nội dung chính.
- [ ] Mọi ảnh quan trọng có alt text.
- [ ] Không có liên kết hỏng.
- [ ] Giá không hiển thị thành miễn phí đối với sản phẩm báo giá.
- [ ] Danh sách đầu dòng không có khoảng cách bất thường.
- [ ] Sản phẩm/giải pháp/bài viết chỉ hiển thị sau khi Published.
- [ ] Các tệp PDF mở và tải được.
- [ ] Email thông báo hoạt động nếu chức năng cần Celery và máy chủ email.
- [ ] Trang hiển thị tốt trên màn hình nhỏ.

## 16. Khi cần hỗ trợ kỹ thuật

Khi báo lỗi cho bộ phận kỹ thuật, nên cung cấp:

1. Tên mục đang sửa, ví dụ **Sản phẩm** hoặc **Giải pháp**.
2. URL trang admin và URL trang công khai.
3. Tên hoặc mã SKU/slug của bản ghi.
4. Ảnh chụp màn hình lỗi.
5. Các bước đã thao tác trước khi lỗi xảy ra.
6. Thời gian xảy ra lỗi.

Không gửi mật khẩu admin, mật khẩu máy chủ hoặc nội dung file `.env` qua kênh công khai.
