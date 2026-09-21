# Contributing / راهنمای مشارکت

## English

Start with the repository skill `nextops-project-context`, the [Markdown context index](docs/MARKDOWN_CONTEXT_INDEX.md), the [development guide](docs/en/DEVELOPMENT.md), the [security guide](docs/en/SECURITY.md), and the [next task](docs/NEXT_TASK.md). Use the server-operations or bilingual-documentation skill when its description matches the change.

Make one bounded change per branch/PR. Explain the requirement, source, expected result and acceptance evidence. Preserve existing work. For documentation, update the corresponding English and Persian guide in the same change; keep commands and identifiers unchanged. The master prompt is the explicit translation exception. Add, rename, or remove the matching entry in `docs/MARKDOWN_CONTEXT_INDEX.md` whenever a project Markdown file changes identity. Run `python3 scripts/check_docs.py` and review Persian wording manually. The script checks project-owned Markdown inventory, structure, and links—not factual or linguistic correctness.

For later code, provide types and tests at the affected boundary. Record real commands/results and distinguish simulated from real-device testing. Do not claim production readiness from documentation or CI alone. Security, local CPU-only AI, offline capability and scoped evidence apply throughout.

Do not post secrets, production inventory, private logs, raw host discovery, weights or database dumps. Do not add a software license or change repository visibility without the owner's decision. Branch protection, required reviews and release automation need separate configuration and verification; templates do not enable them.

## فارسی

ابتدا skill مخزن با نام `nextops-project-context`، [فهرست context Markdown](docs/MARKDOWN_CONTEXT_INDEX.md)، [راهنمای توسعه](docs/fa/DEVELOPMENT.md)، [امنیت](docs/fa/SECURITY.md) و [کار بعدی](docs/NEXT_TASK.md) خوانده شوند. هرجا شرح کار تطبیق دارد از skill عملیات سرور یا مستندات دوزبانه استفاده شود.

هر شاخه یا PR یک تغییر محدود داشته باشد. نیاز، منبع، نتیجهٔ مورد انتظار و شاهد پذیرش را توضیح دهید. کار موجود حفظ شود. تغییر مستندات در نسخهٔ فارسی و انگلیسی هم‌زمان اعمال شود؛ فرمان و شناسه تغییر نکنند. پرامپت اصلی استثنای صریح ترجمه است. با افزودن، تغییر نام یا حذف Markdown متعلق به پروژه، ورودی متناظر `docs/MARKDOWN_CONTEXT_INDEX.md` نیز تغییر کند. ابزار `python3 scripts/check_docs.py` اجرا و متن فارسی دستی بازبینی شود؛ ابزار موجودی Markdown پروژه، ساختار و لینک را می‌سنجد، نه صحت فنی یا زبانی را.

کد آینده باید نوع و آزمون مرزی داشته باشد. فرمان و نتیجهٔ واقعی ثبت و شبیه‌سازی از آزمون تجهیز واقعی جدا شود. مستندات یا CI به‌تنهایی نشانهٔ آمادگی بهره‌برداری نیستند. امنیت، CPU-only محلی، قابلیت آفلاین و دامنهٔ مجاز شواهد در همهٔ مراحل لازم‌اند.

رمز، موجودی عملیاتی، لاگ خصوصی، شناسایی خام سرور، وزن مدل و dump منتشر نشوند. مجوز نرم‌افزاری یا وضعیت عمومی مخزن بدون تصمیم مالک تغییر نکند. حفاظت شاخه، بازبینی الزامی و خودکارسازی انتشار به تنظیم و بررسی جدا نیاز دارند؛ قالب‌ها آن‌ها را فعال نمی‌کنند.
