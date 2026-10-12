# Bias report — Phase B

Nhóm: CC. Người phụ trách: Nguyễn Quốc Cường (2A202602886), Đinh Tiến Cảnh (2A202602918).
Nguồn: `artifacts/judge_results.json`; run timestamp `2026-10-12T16:01:13.420916+00:00`. Generation: `gpt-4o-mini-2024-07-18`; judge: `gpt-4o-mini`. Candidate A lấy từ answers pipeline, B lấy từ `fixtures/human_labels_10q.json:model_answer`, reference từ test set.

## Pairwise swap-and-average

| ID | Candidate A | Candidate B | Ký tự A/B | Pass 1 | Pass 2 quy về A/B | Final | Nhất quán |
|---:|---|---|---:|---|---|---|---|
| 1 | Nhân viên được nghỉ 3 ngày làm việc khi kết hôn. | Nhân viên được nghỉ 3 ngày làm việc có lương khi kết hôn. | 48/57 | B | B | B | có |
| 5 | Cần Tổng Giám đốc (CEO) phê duyệt. | Cần Giám đốc phòng ban phê duyệt. | 34/33 | A | A | A | có |
| 12 | Thưởng Tết tối thiểu cho nhân viên chính thức có thời gian làm việc từ 6 tháng trở lên là **1 tháng lương**. | Nhân viên được thưởng Tết tối thiểu 1 tháng lương. | 108/50 | A | A | A | có |
| 21 | Nhân viên Senior có 9 năm thâm niên sẽ được nghỉ tổng cộng **18 ngày phép năm** (15 ngày phép cơ bản + 3 ngày phép cộng thêm do thâm niên). Về lương, nhân viên này sẽ được hưởng **lương** trong thời gian nghỉ phép năm. | Được nghỉ 18 ngày phép (15 cơ bản + 3 thâm niên). Lương Senior từ 20 đến 35 triệu. | 218/82 | A | B | tie | không |
| 41 | Nhân viên chính thức được hưởng 12 ngày phép năm có lương. | Nhân viên được nghỉ 12 ngày phép năm. | 58/37 | B | A | tie | không |

Position inconsistency: `2/5 = 0.4`. Swap-and-average đã chuyển hai case không ổn định thành tie, thay vì tin một thứ tự. Verbosity win rate là `3/3 = 1.0` trong ba case decisive: A dài hơn và thắng hai case, B dài hơn và thắng một case. Đây là dấu hiệu tương quan với độ dài, không chứng minh nhân quả vì các answer dài hơn cũng chứa chi tiết quan trọng.

| ID | Scores pass 1 (A/B) | Scores pass 2 quy về A/B | Reasoning hai lượt |
|---:|---:|---:|---|
| 1 | 0.75/1.00 | 0.80/1.00 | Cả hai lượt chọn B vì bổ sung thông tin nghỉ có lương. |
| 5 | 1.00/0.00 | 1.00/0.20 | Cả hai lượt chọn A vì đúng thẩm quyền CEO cho mức trên 50 triệu. |
| 12 | 1.00/0.70 | 1.00/0.70 | Cả hai lượt chọn A vì nêu đủ điều kiện làm việc từ 6 tháng. |
| 21 | 0.90/0.70 | 0.80/1.00 | Lượt đầu ưu tiên diễn giải phép của A; lượt sau ưu tiên khoảng lương và độ trực tiếp của B. |
| 41 | 0.30/0.50 | 0.40/0.30 | Cả hai answer đều dùng policy cũ; hai lượt đổi ưu tiên theo độ ngắn gọn và chi tiết có lương. |

## Calibration trên đúng supplied model_answer

| ID | Model answer gốc | Reasoning của judge | Judge | Human | Kết quả |
|---:|---|---|---:|---:|---|
| 1 | Nhân viên được nghỉ 3 ngày làm việc có lương khi kết hôn. | Chính xác theo tài liệu, nêu số ngày nghỉ và điều kiện không trừ phép năm. | 1 | 1 | khớp |
| 5 | Cần Giám đốc phòng ban phê duyệt. | Sai vì đơn hàng trên 50 triệu cần Tổng Giám đốc phê duyệt. | 0 | 0 | khớp |
| 12 | Nhân viên được thưởng Tết tối thiểu 1 tháng lương. | Chính xác và không thiếu ý thiết yếu so với reference. | 1 | 1 | khớp |
| 21 | Được nghỉ 18 ngày phép (15 cơ bản + 3 thâm niên). Lương Senior từ 20 đến 35 triệu. | Chính xác, đủ số ngày phép và khoảng lương Senior. | 1 | 1 | khớp |
| 23 | Hoàn trả 25 triệu vì chưa đủ 1 năm cam kết. | Chính xác, phải hoàn 25 triệu vì chưa đủ thời gian cam kết. | 1 | 1 | khớp |
| 29 | Trưởng phòng phê duyệt. Phạt 2% tháng trên 8 triệu. | Sai vì thiếu Kế toán trưởng và diễn giải sai mốc quá hạn 15 ngày. | 0 | 0 | khớp |
| 33 | Phép: 19 ngày. Phụ cấp: 1.500.000 VNĐ/tháng. | Đúng số ngày phép và tổng phụ cấp theo reference. | 1 | 1 | khớp |
| 41 | Nhân viên được nghỉ 12 ngày phép năm. | Sai vì dùng policy v2023 thay vì policy v2024 hiện hành với 15 ngày. | 0 | 0 | khớp |
| 46 | Nhân viên thử việc không được nghỉ phép năm và phải xin nghỉ không lương nếu cần. | Chính xác; reference còn yêu cầu trưởng phòng phê duyệt khi xin nghỉ. | 1 | 1 | khớp |
| 50 | Được, miễn là đảm bảo kết nối an toàn. | Sai vì policy cấm sử dụng VPN cá nhân. | 0 | 0 | khớp |

Judge labels và human labels đều là `[1,0,1,1,1,0,1,0,1,0]`. Observed agreement `p_o=1.0`; marginal hai bên cùng có 6 positive và 4 negative nên chance agreement `p_e=0.6²+0.4²=0.52`; Cohen’s κ `(1-0.52)/(1-0.52)=1.0`. Kết quả vượt mốc bonus `0.6`.

Giới hạn: chỉ có 5 pairwise pairs và 10 calibration samples; cùng model/prompt có thể cho kết quả khác khi provider snapshot thay đổi. Kappa hoàn hảo trên tập nhỏ không đảm bảo generalization. Cần mở rộng human labels, giữ reference, version và negation cases, đồng thời tiếp tục swap order.
