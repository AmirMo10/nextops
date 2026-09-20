# Publication validation / اعتبارسنجی انتشار مستندات

Date: 2026-09-20. Reviewed publication commit: `392b8c2f044fae62fe019a950e71ec3a9a6e34b2`.

## English

### Verified in this session

The connected GitHub account successfully accepted documentation commits on `AmirMo10/nextops`, branch `main`. The repository was already empty and public before initialization; its visibility was not changed.

GitHub's non-truncated directory-tree responses confirmed the same 16 guide filenames under `docs/en` and `docs/fa`: ARCHITECTURE, CONFIGURATION, CPU_AI, DATA_API, DEVELOPMENT, GLOSSARY, INDEX, INSTALL, INTEGRATIONS, MCP, OPERATIONS, ROADMAP, SECURITY, TESTING, TROUBLESHOOTING and UI.

The published master prompt has exactly 80,536 bytes and Git blob ID `d6420b4436907c8a9daa5599dc8e7398b540b280`, matching the Git blob ID calculated from the supplied source file. Its source SHA-256 is `35d7f8be94145bacc53ca4447695abbcab6115b1a3812a087251ddc2850c54c4`. The original file, including its existing Persian appendix, is unchanged; no new prompt translation was created.

The repository includes a 51-section requirements traceability table, six proposed architecture decisions, bilingual project-control documents and a local documentation-structure checker.

### Not executed or established

The full local documentation checker was not run against a downloaded repository: the working environment could not resolve GitHub for cloning, and the alternative archive-download path was unavailable. Therefore this report does not claim a successful automated link, RTL-rendering or documentation test run. Run `python3 scripts/check_docs.py` from an authorized clone and record the actual result. This script checks local link targets, filenames and wrappers; it does not assess technical accuracy, browser rendering or native-language quality.

No application tests, model evaluation, G10 inspection, CPU benchmark, real-device test, deployment or backup/restore drill was performed. Application CI, branch protection and private vulnerability reporting were not configured by this documentation task. See [project state](PROJECT_STATE.md) and [next task](NEXT_TASK.md).

## فارسی

### موارد بررسی‌شده در این نشست

حساب متصل GitHub ثبت مستندات را در شاخهٔ `main` مخزن `AmirMo10/nextops` پذیرفت. مخزن پیش از شروع کار، خالی و عمومی بود و وضعیت عمومی آن تغییر نکرد.

پاسخ کامل فهرست پوشه‌های GitHub نشان داد که هر ۱۶ نام راهنما در دو پوشهٔ `docs/en` و `docs/fa` همتا دارند: معماری، پیکربندی، هوش مصنوعی روی CPU، داده و API، توسعه، واژه‌نامه، فهرست، نصب، اتصال به سامانه‌ها، MCP، بهره‌برداری، نقشهٔ راه، امنیت، آزمون، عیب‌یابی و رابط کاربری.

پرامپت منتشرشده دقیقاً ۸۰٬۵۳۶ بایت دارد و شناسهٔ Git blob آن با مقدار محاسبه‌شده از فایل دریافت‌شده یکسان است. شناسه و هش SHA-256 در بخش انگلیسی بالا ثبت شده‌اند. فایل اصلی، از جمله پیوست فارسی موجود، بدون تغییر حفظ شده و ترجمهٔ تازه‌ای برای پرامپت تهیه نشده است.

مخزن شامل جدول ردیابی ۵۱ بخش نیازمندی، شش تصمیم معماری پیشنهادی، اسناد کنترلی دوزبانه و ابزار محلی بررسی ساختار مستندات است.

### موارد اجرا‌نشده یا احرازنشده

بررسی کامل مستندات روی نسخهٔ دریافت‌شده از مخزن اجرا نشد؛ محیط کاری نتوانست برای clone نام GitHub را resolve کند و مسیر جایگزین دریافت آرشیو نیز در دسترس نبود. بنابراین موفقیت آزمون خودکار لینک‌ها، نمایش راست‌به‌چپ یا مستندات ادعا نمی‌شود. فرمان `python3 scripts/check_docs.py` در نسخهٔ مجاز مخزن اجرا و نتیجهٔ واقعی ثبت شود. این ابزار مقصد لینک محلی، نام فایل و پوشش RTL را بررسی می‌کند؛ صحت فنی، نمایش مرورگر یا طبیعی بودن زبان را نمی‌سنجد.

آزمون برنامه، ارزیابی مدل، بررسی G10، سنجش کارایی CPU، آزمون تجهیز واقعی، استقرار یا تمرین پشتیبان و بازیابی انجام نشده است. CI برنامه، حفاظت شاخه و گزارش خصوصی آسیب‌پذیری نیز در این کار مستندسازی تنظیم نشده‌اند. [وضعیت پروژه](PROJECT_STATE.md) و [کار بعدی](NEXT_TASK.md) را ببینید.
