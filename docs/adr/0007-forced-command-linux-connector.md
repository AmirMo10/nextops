# ADR 0007 — Forced-command Linux diagnostics

Status: accepted for Phase 2 implementation on 2026-09-23. Source: master sections 13–16 and the
owner's instruction to complete Phase 2.

## English

### Context

Phase 2 requires current Linux evidence from the four approved guests. Giving the application,
model or connector an unrestricted shell would violate the existing authorization and credential
boundaries. Reusing the full deployment account would also make a read-only feature depend on an
administrative identity.

### Decision

Use a dedicated non-login `nextops-linux-ro` identity on each approved target. Its SSH key is
accepted only with a server-side forced command, no PTY, forwarding, agent forwarding or user-
selected command. The forced command runs a versioned local collector that returns one bounded JSON
snapshot. The connector owns distinct per-target private keys and strict host-key pins, resolves
only deployment-configured target IDs, and exposes named read operations rather than SSH arguments.

The application requires both `zabbix.read` and `linux.read`, selects only a configured immutable
target ID, persists the run before collection, and stores the exact bounded Zabbix/Linux evidence
with its hash and audit record. The model receives sanitized evidence, never credentials, command
selection or network destinations.

### Alternatives

- Reuse the deployment account: rejected because it has administrative authority.
- Expose an allowlisted generic command API: rejected because argument parsing and command growth
  create a larger execution surface.
- Use only Zabbix Agent items: retained as corroborating evidence, but rejected as the sole Phase 2
  Linux path because it does not provide the required direct diagnostic boundary.
- Install a privileged agent: rejected for this phase; the required evidence is available to a
  narrow unprivileged collector.

### Consequences

The design adds key and host-pin lifecycle work for every target and requires the collector to stay
backward compatible with its typed contract. In return, target choice, command choice and output
limits remain deterministic outside the model. Failure of one Linux target can be reported as
partial evidence without granting a fallback shell.

### Security and operations

Collector output is size-limited, timestamps are UTC, source text is untrusted, journal messages are
redacted and bounded, and all subprocess calls use constant argument arrays with timeouts. Rollback
removes the additive app/connector release and target authorization; target accounts and keys are
disabled only after the prior release is restored and verified. No write or remediation operation is
introduced.

## فارسی

### زمینه

مرحلهٔ دو به شواهد جاری Linux از چهار مهمان مصوب نیاز دارد. دادن shell آزاد به برنامه، مدل یا
اتصال‌دهنده با مرزهای مجوز و اطلاعات ورود سازگار نیست. استفاده از حساب کامل استقرار نیز یک قابلیت
فقط‌خواندنی را به هویت مدیریتی وابسته می‌کند.

### تصمیم

روی هر مقصد مصوب، هویت بدون ورود `nextops-linux-ro` ساخته می‌شود. کلید SSH آن فقط همراه فرمان
اجباری سمت سرور پذیرفته می‌شود و PTY، انتقال درگاه، agent forwarding و فرمان انتخابی کاربر ندارد.
فرمان اجباری یک گردآورندهٔ محلی و نسخه‌دار را اجرا می‌کند و تنها یک snapshot محدود JSON
برمی‌گرداند. اتصال‌دهنده برای هر مقصد کلید خصوصی جدا و کلید میزبان تثبیت‌شده دارد، فقط شناسه‌های
پیکربندی‌شده را می‌شناسد و به‌جای آرگومان SSH، عملیات خواندن نام‌دار ارائه می‌کند.

برنامه هر دو دامنهٔ `zabbix.read` و `linux.read` را لازم می‌داند، فقط مقصد ثابت‌شده در استقرار را
می‌پذیرد، پیش از گردآوری اجرای ماندگار می‌سازد و شواهد محدود Zabbix و Linux را همراه هش و ممیزی
ذخیره می‌کند. مدل هرگز اطلاعات ورود، انتخاب فرمان یا مقصد شبکه را دریافت نمی‌کند.

### گزینه‌های کنارگذاشته‌شده

- حساب استقرار، به‌دلیل اختیار مدیریتی آن، استفاده نمی‌شود.
- API عمومیِ «فرمان مجاز» به‌دلیل گسترش سطح اجرا و دشواری کنترل آرگومان رد می‌شود.
- دادهٔ Agent زبیکس برای تطبیق مفید است، اما جای مرز مستقیم عیب‌یابی Linux را نمی‌گیرد.
- agent دارای امتیاز در این مرحله نصب نمی‌شود؛ شاهد لازم با گردآورندهٔ محدود و بدون امتیاز قابل
  دریافت است.

### پیامد و عملیات

چرخهٔ عمر کلید و pin میزبان برای هر مقصد و سازگاری قرارداد گردآورنده کار عملیاتی تازه است. در
مقابل، مقصد، فرمان و سقف خروجی بیرون مدل و به‌صورت قطعی کنترل می‌شوند. شکست یک مقصد به شاهد ناقص
می‌انجامد، نه shell جایگزین. خروجی سقف دارد، زمان‌ها UTC هستند، متن منبع دادهٔ غیرقابل‌اعتماد است،
پیام journal پالایش و محدود می‌شود و subprocess فقط با آرگومان ثابت و مهلت اجرا فراخوانی می‌شود.
بازگشت ابتدا انتشار قبلی را فعال و تأیید می‌کند و سپس دسترسی افزوده را غیرفعال می‌سازد. هیچ عملیات
نوشتنی یا اصلاحی در این تصمیم افزوده نمی‌شود.
