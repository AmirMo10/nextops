# ADR 0001 — Modular core and single-host deployment

Status: accepted on 2026-09-21. Source: master sections 3, 5–7, 18, 20.

## English

Use a modular control plane with separate durable worker, protected MCP gateway, enabled connector runners and local inference. Split for trust/resource boundaries, not one microservice per feature. Keep domain/application dependencies inward and contracts typed.

The initial G10 is one failure domain even with separate containers or VMs. Separate environments logically, retain future separate-host interfaces and require an off-host backup decision. Do not add Kubernetes, service mesh, Kafka or a graph engine without demonstrated need. Consequence: simpler initial operations, but no claim of host-level high availability.

## فارسی

وضعیت: پذیرفته‌شده در ۲۱ سپتامبر ۲۰۲۶. هستهٔ مدیریتی ماژولار، worker ماندگار جدا، درگاه MCP حفاظت‌شده، اتصال‌های لازم و مدل محلی انتخاب می‌شوند. جداسازی بر اساس اعتماد و منابع است، نه یک ریزسرویس برای هر ویژگی. وابستگی رو به دامنه و قرارداد دارای نوع حفظ شود.

G10 اولیه حتی با چند کانتینر یا VM یک نقطهٔ خرابی است. محیط‌ها منطقی جدا و امکان انتقال آینده به میزبان مستقل حفظ شود. مقصد پشتیبان بیرونی تصمیم الزامی است. Kubernetes، مش سرویس، Kafka یا موتور گراف بدون نیاز اثبات‌شده اضافه نشود. پیامد: عملیات اولیه ساده‌تر، اما بدون ادعای دسترس‌پذیری بالای میزبان.
