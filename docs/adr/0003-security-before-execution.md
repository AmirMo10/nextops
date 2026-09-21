# ADR 0003 — Security before infrastructure execution

Status: accepted on 2026-09-21. Source: master sections 3, 11–14, 20–21.

## English

Move scoped identity, deterministic policy, credential isolation, durable audit and approval contracts before real infrastructure access. The model proposes but cannot grant permission, lower risk or change its policy. MVP mutations stay disabled.

Read-only labels do not authorize arbitrary commands or SQL. Admin does not bypass controls. Later changes need exact-action approval with revalidated permissions/pre-state and atomic single-use consumption. Unknown remote outcomes require reconciliation, not blind retry. Consequence: a smaller initial tool catalog and more explicit contracts, in exchange for an enforceable safety boundary rather than a prompt-only promise.

## فارسی

وضعیت: پذیرفته‌شده در ۲۱ سپتامبر ۲۰۲۶. هویت محدود، سیاست قطعی، جداسازی اطلاعات ورود، ممیزی ماندگار و قرارداد تأیید پیش از دسترسی واقعی زیرساخت ساخته می‌شوند. مدل پیشنهاد می‌دهد، اما حق اعطای مجوز، کاهش ریسک یا تغییر سیاست خودش ندارد. تغییرات در MVP غیرفعال می‌مانند.

برچسب فقط‌خواندنی مجوز فرمان یا SQL دلخواه نیست. مدیر از کنترل مستثنا نیست. تغییر بعدی به تأیید دقیق، بررسی دوبارهٔ مجوز و وضعیت اولیه و مصرف اتمی یک‌بارمصرف نیاز دارد. نتیجهٔ نامشخص راه دور باید بررسی شود، نه تکرار کورکورانه. پیامد: فهرست ابزار اولیه کوچک‌تر و قرارداد صریح‌تر، در برابر مرز ایمنی واقعی به‌جای وعدهٔ صرفاً پرامپتی.
