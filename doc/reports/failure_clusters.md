# Phân tích failure clusters — Phase A

Nhóm: CC. Người phụ trách: Đinh Tiến Cảnh (2A202602918), Nguyễn Quốc Cường (2A202602886).
Nguồn: `artifacts/ragas_50q.json`; run timestamp: `2026-10-12T16:00:29.012374+00:00`. Generation live, không fallback: `gpt-4o-mini-2024-07-18`; evaluator: `gpt-4o-mini`, `text-embedding-3-small`.

## Kết quả theo distribution

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---:|---:|---:|
| faithfulness | 0.8750 | 0.5042 | 0.8000 |
| answer_relevancy | 0.4898 | 0.4709 | 0.3786 |
| context_precision | 0.8958 | 0.9167 | 0.6833 |
| context_recall | 1.0000 | 0.8458 | 0.6833 |
| avg_score | 0.8152 | 0.6844 | 0.6363 |

## Bottom 10

| Rank | ID | Câu hỏi | Distribution | Avg | Worst metric | Chẩn đoán / hướng sửa |
|---:|---:|---|---|---:|---|---|
| 1 | 22 | Nếu cần mua một chiếc laptop 30 triệu cho nhân viên mới, ai phê duyệt và cần gì từ phòng CNTT? | multi_hop | 0.0833 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 2 | 49 | Theo chính sách nghỉ phép cũ (v2023), nhân viên được nghỉ bao nhiêu ngày? Còn chính sách nào đang có hiệu lực hiện tại? | adversarial | 0.0833 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 3 | 25 | Lương thử việc của nhân viên Junior mức cao nhất là bao nhiêu? | multi_hop | 0.3750 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 4 | 33 | Nhân viên Manager có thâm niên 12 năm: tổng phụ cấp hàng tháng và số ngày phép năm theo v2024 là bao nhiêu? | multi_hop | 0.3750 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 5 | 50 | Nhân viên Manager có thể dùng VPN cá nhân (như NordVPN) khi WFH để tăng bảo mật thêm không? | adversarial | 0.4167 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 6 | 31 | Nhân viên đi công tác trong nước, ở khách sạn 2 đêm với giá 1.500.000 VNĐ/đêm. Công ty thanh toán tối đa bao nhiêu cho tiền khách sạn? | multi_hop | 0.4361 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 7 | 40 | Nhân viên cấp Manager có thời hạn thử việc 90 ngày, đang trong tháng thứ 3, phát hiện vi phạm bảo mật. Họ nên và không nên làm gì theo chính sách? | multi_hop | 0.4583 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 8 | 9 | Nam nhân viên được nghỉ bao nhiêu ngày khi vợ sinh con? | factual | 0.5000 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 9 | 7 | Nghỉ phép không lương 20 ngày cần ai phê duyệt? | factual | 0.5814 | faithfulness | LLM hallucinating; Tighten system prompt, lower temperature |
| 10 | 43 | Mật khẩu phải có tối thiểu bao nhiêu ký tự? | adversarial | 0.6240 | context_precision | Too many irrelevant chunks; Add reranking or metadata filter |

Đối chiếu ba case đại diện:

- ID 22 trả lời “Không tìm thấy”, trong khi reference yêu cầu Director phê duyệt, ba báo giá và xác nhận CNTT. Ba context lấy về là sổ tay an toàn, nghỉ không lương và tạm ứng, không có policy mua sắm; đây là lỗi retrieval dẫn tới answer thiếu căn cứ.
- ID 49 cũng trả lời “Không tìm thấy”. Context chỉ gồm bảo hiểm, thử việc và nghỉ ốm, không chứa hai policy phép năm v2023/v2024 cần để trả lời; lỗi chính là context recall.
- ID 43 trả lời đúng 12 ký tự. Context chứa cả mật khẩu v1 đã thay thế và v2 hiện hành, cộng một tài liệu không liên quan; vì vậy `context_precision` là metric thấp nhất dù generation đã chọn đúng policy v2.

Các case này cho thấy không thể quy mọi lỗi cho generation: ID 22/49 thiếu tài liệu cần thiết, còn ID 43 có context thừa và xung đột phiên bản.

## Matrix worst metric × distribution

| Worst metric | factual | multi_hop | adversarial |
|---|---:|---:|---:|
| faithfulness | 3 | 11 | 2 |
| context_recall | 0 | 1 | 1 |
| context_precision | 2 | 0 | 2 |
| answer_relevancy | 15 | 8 | 5 |

Nhóm yếu theo mean là **adversarial**, mean `0.6363`; đây là so sánh quality mean, không dùng tổng cột 20/20/10. Worst metric xuất hiện nhiều nhất là **answer_relevancy** với 28 câu. Adversarial mean thấp hơn factual (`0.6363 < 0.8152`), phù hợp bonus Phase A, nhưng chỉ chứng minh tập adversarial khó hơn chứ không tự chứng minh pipeline nhận biết version conflict.

Hướng sửa ưu tiên: gắn metadata `effective_version`, filter policy hết hiệu lực; decomposition cho multi-hop; yêu cầu answer trích support theo từng mệnh đề; và regression-test lại các ID 22, 25, 33, 43, 49, 50.
