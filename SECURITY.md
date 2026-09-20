# Security policy / سیاست امنیت

## English

The repository currently contains design documentation, not a supported production release. No operational security guarantees or supported software versions are claimed. See [security design](docs/en/SECURITY.md).

Never disclose credentials, production addresses, private logs or exploit details involving real infrastructure in a public issue. Use an owner-approved private channel for sensitive reports. GitHub private vulnerability reporting has not been verified as enabled; do not assume a reporting endpoint exists.

A safe report includes a sanitized description, affected commit or document, expected versus observed behavior and non-sensitive reproduction steps. Do not test against infrastructure without authorization. If a credential was exposed, revoke/rotate it through its owning system; removing text from a commit is not a substitute.

The master prompt and examples contain requirements, not live inventory. All AI stays on local CPUs; the LLM never owns target credentials or grants permissions. Infrastructure changes remain disabled until their separate approval gates are implemented and validated.

## فارسی

مخزن فعلاً مستندات طراحی دارد و نسخهٔ عملیاتی پشتیبانی‌شده نیست. هیچ تضمین امنیت عملیاتی یا فهرست نسخهٔ نرم‌افزاری پشتیبانی‌شده ادعا نمی‌شود. [طرح امنیت](docs/fa/SECURITY.md) را ببینید.

اطلاعات ورود، نشانی عملیاتی، لاگ خصوصی یا جزئیات سوءاستفاده از زیرساخت واقعی در issue عمومی منتشر نشود. گزارش حساس از مسیر خصوصیِ تأییدشده توسط مالک ارسال شود. فعال بودن گزارش خصوصی آسیب‌پذیری GitHub بررسی نشده است؛ وجود مسیر گزارش فرض نشود.

گزارش ایمن شامل شرح پالایش‌شده، commit یا سند درگیر، انتظار در برابر مشاهده و روش بازتولید غیرحساس است. زیرساخت بدون مجوز آزموده نشود. اطلاعات ورود افشاشده باید در سامانهٔ مالک باطل یا تعویض شود؛ حذف متن commit جای آن را نمی‌گیرد.

پرامپت و نمونه‌ها نیازمندی‌اند، نه موجودی واقعی. همهٔ هوش مصنوعی روی CPU محلی می‌ماند. مدل اطلاعات ورود مقصد ندارد و مجوز صادر نمی‌کند. تغییر زیرساخت تا ساخت و اعتبارسنجی مرحلهٔ مستقل تأیید، غیرفعال است.
