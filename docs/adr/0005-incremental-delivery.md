# ADR 0005 — Complete flows and controlled release

Status: accepted on 2026-09-21. Source: master sections 3–4, 8, 22–26.

## English

Replace the original late-security/late-offline sequence with phases 0–8 and cross-cutting tests/docs/security. Preserve all eleven integrations but begin with a complete read-only Persian Zabbix/Linux investigation. Obtain architecture approval before implementation and separate lab validation from production authorization.

Use small branches/PRs and explicitly promoted verified releases. Untrusted PR checks run in isolated disposable workers without management reachability. Hardware tests on the G10 require a trusted resource-limited path. No automatic production deployment on push. Consequence: useful tested increments and safer collaboration; setting up documentation does not enable CI, branch protection or release credentials.

## فارسی

وضعیت: پذیرفته‌شده در ۲۱ سپتامبر ۲۰۲۶. ترتیب اولیهٔ امنیت و آفلاینِ دیرهنگام با مراحل صفر تا هشت و آزمون و مستندات و امنیت در همهٔ مراحل جایگزین می‌شود. یازده اتصال حفظ می‌شوند، اما شروع با بررسی کامل فارسی و فقط‌خواندنی Zabbix/Linux است. پیش از ساخت، معماری تأیید شود و آزمون آزمایشگاه از اجازهٔ بهره‌برداری جدا بماند.

شاخه و PR کوچک و انتخاب صریح نسخهٔ تأییدشده به‌کار رود. PR نامطمئن در worker موقت و بدون مسیر مدیریت آزموده شود. آزمون G10 مسیر معتبر و محدود می‌خواهد. push به استقرار خودکار عملیاتی منجر نمی‌شود. پیامد: تحویل مفید و آزموده و همکاری ایمن‌تر؛ مستندسازی به‌تنهایی CI، حفاظت شاخه یا اطلاعات ورود انتشار را فعال نمی‌کند.
