# ADR 0004 — PostgreSQL-first authoritative state

Status: proposed. Source: master sections 3, 6, 11, 16.

## English

Use PostgreSQL initially for business state, durable jobs, approvals, audit and topology/retrieval metadata, with SQLAlchemy/Alembic and tested constraints/migrations. Cache is not an authority. Keep database abstractions without asserting MySQL/SQLite parity before conformance tests.

Managed SQL Server and MySQL/MariaDB are separate connector requirements, not internal backend choices. Begin topology relationally and add vector capability only when justified. Consequence: fewer operational systems and one tested consistency model; alternate internal backends are deferred explicitly rather than silently removed.

## فارسی

وضعیت: پیشنهادی. PostgreSQL مرجع اولیهٔ وضعیت، کار ماندگار، تأیید، ممیزی و فرادادهٔ توپولوژی و بازیابی است و با SQLAlchemy/Alembic و قید و migration آزموده به‌کار می‌رود. cache مرجع معتبر نیست. رابط پایگاه حفظ می‌شود، اما هم‌ارزی MySQL/SQLite پیش از آزمون انطباق ادعا نمی‌شود.

SQL Server و MySQL/MariaDB تحت مدیریت، نیاز اتصال جدا هستند و با انتخاب پایگاه داخلی اشتباه نمی‌شوند. توپولوژی ابتدا رابطه‌ای است و قابلیت برداری فقط در صورت نیاز اضافه می‌شود. پیامد: سامانهٔ عملیاتی کمتر و مدل سازگاری آزموده؛ پایگاه‌های داخلی جایگزین صریحاً به آینده موکول می‌شوند، نه حذف بی‌صدا.
