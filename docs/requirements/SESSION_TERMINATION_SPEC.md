# Server-side session termination / پایان‌دادن نشست در سمت سرور

Status: **source implemented; PostgreSQL CI and controlled deployment pending.** Date: 2026-09-23.

## English

### Problem statement

The panel stored its opaque bearer only in the current browser tab, but its sign-out action removed
only that browser copy. Until expiry, a copied token could still authenticate because the durable
server-side session was not revoked. Production-grade sign-out must terminate the presented session
at the authoritative PostgreSQL boundary and leave an audit record.

### Requirements and threat considerations

- `POST /api/v1/logout` requires a bearer header, hashes the token, and never stores or logs its
  plaintext value.
- Revoke exactly the presented session; other sessions for the same identity remain valid.
- Lock the session row during revocation, make replay idempotent, and emit one append-only
  `identity.logout.accepted` audit event with the request correlation ID.
- Return the same empty success for an unknown well-formed bearer as for a revoked session so the
  endpoint does not become a token-existence oracle. A missing bearer remains a structured `401`.
- The browser calls the server before removing its tab-local value. Local removal still occurs if
  the server is unavailable, but that failure must not be misrepresented as server-side revocation.
- Keep session expiry, password recovery, credential-version revocation, scopes, and all connector
  and model boundaries unchanged.

### Non-goals

This increment does not implement global sign-out, an administrator session console, refresh
tokens, federated identity, idle-timeout renewal, browser cookies, or certificate rotation. It adds
no database migration and does not change the configured absolute session lifetime.

### Implementation and tests

The existing durable service performs a single transaction using the SHA-256 token index, a row
lock, the existing `revoked_at` field, and the append-only audit table. The FastAPI boundary exposes
only an empty `204`. The static offline panel awaits the request and clears `sessionStorage` in a
`finally` block.

Boundary tests verify missing-bearer denial, the exact token/correlation handoff, empty response,
and local static wiring. PostgreSQL integration verifies that only the presented session is
invalidated, a different session remains usable, replay creates no second audit event, and the
audit contains no token data. Real-browser acceptance verifies one logout request, removal of the
tab-local token, and return to the localized login view.

### Acceptance, rollback, and documentation

Source acceptance requires Ruff, strict typing, unit/API tests, PostgreSQL 16 and 17 integration
jobs, real-browser acceptance, secret scanning, and paired documentation. Controlled deployment
acceptance additionally requires a real login/logout, rejection of the former token through a
protected API, persistence of exactly one sanitized audit event, service health, and immutable
rollback. Rollback restores the prior application release only; no schema rollback is needed.

## فارسی

<div dir="rtl">

### شرح مسئله

پنل، bearer مبهم نشست را فقط در برگهٔ فعلی مرورگر نگه می‌داشت، اما دکمهٔ خروج فقط همان نسخهٔ
مرورگر را حذف می‌کرد. تا پایان اعتبار، نسخهٔ کپی‌شدهٔ توکن همچنان می‌توانست احرازهویت شود، زیرا
نشست ماندگار سمت سرور لغو نمی‌شد. خروج در سطح تولید باید نشست ارائه‌شده را در مرجع PostgreSQL
پایان دهد و شاهد ممیزی ثبت کند.

### نیازمندی‌ها و ملاحظات تهدید

- مسیر `POST /api/v1/logout` به bearer نیاز دارد، توکن را hash می‌کند و مقدار روشن آن را ذخیره یا
  ثبت نمی‌کند.
- فقط همان نشست ارائه‌شده لغو شود و نشست‌های دیگر همان هویت معتبر بمانند.
- سطر نشست هنگام لغو قفل، تکرار درخواست idempotent و فقط یک رویداد ممیزیِ فقط‌افزودنی با نام
  `identity.logout.accepted` و شناسهٔ هم‌بستگی درخواست ثبت شود.
- پاسخ bearer ناشناخته اما درست‌ساخت با نشست لغوشده یکسان و خالی باشد تا مسیر به ابزار تشخیص وجود
  توکن تبدیل نشود. نبود bearer همچنان `401` ساخت‌یافته برمی‌گرداند.
- مرورگر پیش از حذف مقدار محلی، سرور را فراخوانی کند. اگر سرور در دسترس نبود، پاک‌سازی محلی همچنان
  انجام می‌شود؛ اما این حالت نباید به‌عنوان لغو سمت سرور معرفی شود.
- انقضای نشست، بازیابی گذرواژه، لغو بر پایهٔ نسخهٔ اعتبارنامه، scopeها و همهٔ مرزهای اتصال‌دهنده و
  مدل بدون تغییر بمانند.

### خارج از دامنه

این increment خروج از همهٔ نشست‌ها، پنل مدیریت نشست، refresh token، هویت فدرال، تمدید مهلت بیکاری،
cookie مرورگر یا چرخش گواهی را پیاده نمی‌کند. migration پایگاه ندارد و طول عمر مطلق نشست را تغییر
نمی‌دهد.

### پیاده‌سازی و آزمون

سرویس ماندگار موجود، یک تراکنش را با شاخص SHA-256 توکن، قفل سطر، فیلد موجود `revoked_at` و جدول
ممیزی فقط‌افزودنی اجرا می‌کند. مرز FastAPI فقط پاسخ خالی `204` ارائه می‌دهد. پنل ایستای آفلاین
منتظر پاسخ می‌ماند و در بلوک `finally` مقدار `sessionStorage` را پاک می‌کند.

آزمون مرزی، رد درخواست بدون bearer، تحویل دقیق توکن و شناسهٔ هم‌بستگی، پاسخ خالی و اتصال فایل
ایستا را بررسی می‌کند. آزمون یکپارچگی PostgreSQL ثابت می‌کند فقط نشست ارائه‌شده نامعتبر می‌شود،
نشست دیگر معتبر می‌ماند، تکرار درخواست رویداد دوم نمی‌سازد و ممیزی دادهٔ توکن ندارد. آزمون واقعی
مرورگر نیز یک درخواست خروج، حذف توکن برگه و بازگشت به نمای بومی‌شدهٔ ورود را می‌سنجد.

### پذیرش، بازگشت و مستندات

پذیرش منبع به Ruff، بررسی سخت‌گیرانهٔ نوع، آزمون واحد و API، کارهای یکپارچگی PostgreSQL 16 و 17،
مرورگر واقعی، پویش راز و مستندات دوزبانه نیاز دارد. پذیرش استقرار کنترل‌شده افزون بر آن باید ورود
و خروج واقعی، رد توکن قبلی در یک API محافظت‌شده، ثبت دقیق یک رویداد ممیزی پالایش‌شده، سلامت سرویس
و بازگشت تغییرناپذیر را ثابت کند. بازگشت فقط انتشار پیشین برنامه را فعال می‌کند و rollback پایگاه
لازم نیست.

</div>
