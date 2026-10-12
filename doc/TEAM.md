# Nhóm thực hiện K4 Track 3B

Tên nhóm: CC
Repo chung: https://github.com/mnic2904/K4-L3-DAY24-CC-Eval-Guard
Trưởng nhóm/người nộp: Đinh Tiến Cảnh
Deadline áp dụng: 11:59 AM ngày 13/10/2026 — Asia/Ho_Chi_Minh (UTC+07:00)
Commit kỹ thuật: Cảnh `6de743a63ef1a31093663a95a05424fab5646773`; Cường `5d71986c88ac017b1a79df7b391f9ccdcf53bd35`. Commit dùng để chấm là HEAD cuối do trưởng nhóm push sau khi hoàn thiện TEAM.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Đinh Tiến Cảnh | 2A202602918 | 50%: Phase A, Phase C, tích hợp và kiểm tra bản nộp | Commit `6de743a`; `src/phase_a_ragas.py`, `src/phase_c_guard.py`, artifacts A/C, failure report và blueprint |
| 2 | Nguyễn Quốc Cường | 2A202602886 | 50%: Phase B, pipeline m1–m5, phân tích và review chéo | Commit `5d71986`; `src/phase_b_judge.py`, `src/m1_chunking.py`–`src/m5_enrichment.py`, artifact B và bias report |

Người tích hợp/chạy batch/nộp link: Đinh Tiến Cảnh; Nguyễn Quốc Cường review artifacts, reports và checker. Hai người cùng chịu trách nhiệm cho kết quả cuối.

## Môi trường và chuẩn bị trước lớp

OS/Python: Windows, Python 3.11; pipeline và các batch live đã chạy thành công.
Virtualenv/dependencies/imports: `.venv` hiện có; `.venv\Scripts\python.exe -m pip check` trả về `No broken requirements found`.
Models/Qdrant/50 answers: Qdrant local khả dụng; embedding BGE-M3 và FlashRank `ms-marco-TinyBERT-L-2-v2` đã chạy. `artifacts/answers_50q.json` có 50 answers live (20/20/10), toàn bộ generation bằng `gpt-4o-mini-2024-07-18`; ba phase artifacts đã được tạo và schema-check.

## INDIVIDUAL

### DinhTienCanh-2A202602918

- Phần được giao và phần thực tế đã làm: 50% khối lượng; Phase A (distribution, RAGAS adapter, bottom 10, cluster), Phase C (PII, rails, adversarial suite, latency), tích hợp.
- Bằng chứng: commit `6de743a63ef1a31093663a95a05424fab5646773`, source Phase A/C, answers tích hợp, artifacts A/C, failure report và blueprint.
- Cách kiểm tra: unit tests Phase A/C, setup answers live, runner A/C live và `scripts/check_lab.py`.
- Điều đã học: phân biệt tần suất worst metric với quality mean; clean controls phát hiện always-block; latency phải có warm-up và scope.
- Giới hạn/cách xử lý: tập đánh giá còn nhỏ; đã chạy live, đối chiếu schema và checker, không tạo kết quả giả.
- Nguồn/AI hỗ trợ nếu có: Codex hỗ trợ implementation/review; nhóm tự kiểm chứng bằng tests, schema và checker.

### NguyenQuocCuong-2A202602886

- Phần được giao và phần thực tế đã làm: 50% khối lượng; Phase B (pairwise, swap, kappa, bias), pipeline m1–m5, phân tích và review chéo.
- Bằng chứng: commit `5d71986c88ac017b1a79df7b391f9ccdcf53bd35`, source Phase B/m1–m5, artifact B và bias report.
- Cách kiểm tra: unit tests Phase B/pipeline, runner B live, đối chiếu 10 supplied answers với human labels và `scripts/check_lab.py`.
- Điều đã học: pairwise winner khác nhãn tốt/xấu; swap giúp đo position inconsistency; kappa hiệu chỉnh agreement ngẫu nhiên.
- Giới hạn/cách xử lý: calibration chỉ có 10 mẫu và 5 cặp; report phải nêu độ bất định và không khái quát quá mức.
- Nguồn/AI hỗ trợ nếu có: Codex hỗ trợ implementation/review; nhóm tự kiểm chứng bằng tests, schema và checker.

## Cập nhật sau khi nộp

Chưa nộp và chưa có cập nhật sau nộp. Khi nộp, trưởng nhóm ghi commit SHA và thời điểm gửi; mọi thay đổi sau deadline sẽ được ghi rõ.
