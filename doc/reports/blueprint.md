# Blueprint CI/CD cho RAG và guardrails

Nhóm: CC. Phụ trách chung: Đinh Tiến Cảnh (2A202602918), Nguyễn Quốc Cường (2A202602886). Đây là blueprint CI/CD theo yêu cầu. Toàn bộ pipeline lab đã được cài đặt và chạy live; nhóm không tạo workflow CI tự động ngoài phạm vi bài.
Nguồn: artifacts A/B/C. Run guard `2026-10-12T16:09:34.357139+00:00`; guard `gpt-4o-mini`; generation `gpt-4o-mini-2024-07-18`; evaluator `gpt-4o-mini` + `text-embedding-3-small`; judge `gpt-4o-mini`.

## Kiến trúc và failure action

Input → Presidio (chỉ CCCD/CMND, VN phone, email) → NeMo input → hybrid retrieval BGE-M3 → FlashRank → generation → NeMo output → response. Request thật dừng sớm khi PII hoặc input rail chặn; phép đo Task 12 cố ý chạy cả hai input layers tuần tự.

PII được phát hiện và chặn; nếu triển khai logging thì chỉ ghi dữ liệu đã redact. Jailbreak/off-topic nhận câu từ chối chuẩn. Output nhạy cảm bị thay bằng refusal, output sạch giữ nguyên. API keys chỉ ở `.env`/CI secrets và không commit. Nếu generation API lỗi, pipeline ghi rõ `extractive_fallback` và model null; không dùng ground truth làm answer.

## Phạm vi và latency

Task 12 đo `input_layers_sequential`, 20 timed samples, 2 warm-up thật bị loại, percentile nội suy tuyến tính. Engines được tạo trước khi đo và input guard là tổng theo từng sample.

| Layer / scope | P50 ms | P95 ms | P99 ms | Tình trạng |
|---|---:|---:|---:|---|
| Presidio | 10.691650 | 12.850715 | 13.962063 | đã đo |
| NeMo input | 697.275000 | 1013.807610 | 1124.141522 | bottleneck |
| Input guard sequential | 708.842150 | 1023.170765 | 1131.836553 | vượt budget |
| RAG | chưa đo | chưa đo | chưa đo | ngoài Task 12; không có nghĩa là chưa cài đặt |
| NeMo output | chưa đo | chưa đo | chưa đo | ngoài Task 12; không có nghĩa là chưa cài đặt |
| Full guard / request short-circuit | chưa đo | chưa đo | chưa đo | không suy từ input_guard_ms |

Input-layer target `500 ms`; `budget_ok=false` vì P95 `1023.170765 ms`. NeMo input chiếm gần toàn bộ latency. Bước tiếp theo là cache các policy query an toàn, benchmark model guard nhỏ hơn và đo riêng network/model time. RAG, output và full-request sẽ được đo bằng cùng warm-up/sample/percentile method, không tái sử dụng input P95.

## CI gates đề xuất

CI đề xuất chạy `python -m pytest tests -q`, sau đó batch live theo lịch hoặc khi policy/model thay đổi, cuối cùng `python scripts/check_lab.py`. Gate mục tiêu sẽ fail nếu: faithfulness mean <0.75, overall avg <0.65, attacks <18/20, clean không đạt 8/8, output cases fail, hoặc full-guard P95 vượt 500 ms sau khi metric này được đo. Mốc lab bắt buộc vẫn là attacks 15/20; 18/20 là gate đề xuất/bonus. Bản lab hiện tại dùng `scripts/check_lab.py`; chưa bổ sung workflow hoặc runner CI riêng.

## Monitoring và cải tiến

Theo dõi hàng tuần: RAGAS theo distribution, bottom regressions, kappa trên human sample mới, position inconsistency, attack recall, clean false-positive rate, output leak rate và latency P50/P95/P99. Cảnh báo khi clean FP >0, attacks <90%, kappa <0.6 hoặc metric RAGAS giảm >0.05 so baseline. Log chỉ giữ ID/category/decision/latency, redact PII và giới hạn retention; owner luân phiên hai thành viên review false positives và drift.

Baseline hiện tại: factual `0.8152`, multi-hop `0.6844`, adversarial thấp nhất `0.6363`; Cohen’s κ `1.0`; attacks `20/20`; clean false-positive rate `0.0`; output `4/4`. Tập 50/20/8/4 còn nhỏ nên cần bổ sung paraphrase, Vietnamese không dấu, version-conflict, mixed PII và long-context cases. Cải tiến ưu tiên là metadata version filtering, multi-hop decomposition, regression cho bottom IDs, prompt guard có clean examples và tối ưu NeMo latency.
