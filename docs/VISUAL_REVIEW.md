# Visual documentation review / بازبینی مستندات تصویری

Date: 2026-09-20. Baseline inspected: `f8ff3c463682c96241b1826cb7540f055eaa2327`.

## English

Scope: documentation only. Added [English diagrams](en/DIAGRAMS.md), [Persian diagrams](fa/DIAGRAMS.md), [English stack](en/TECH_STACK.md) and [Persian stack](fa/TECH_STACK.md), with README/index navigation and project bookkeeping. No host access, installation, production call, model inference or runtime dependency change was performed.

### Checks performed on the four new guide sources

A local Python check extracted all Mermaid fences: seven per language, fourteen total. Corresponding diagram types and ordered interaction/transition endpoints matched after localized labels were removed. The conceptual ER diagram was identical in both versions. UTF-8 text, final newlines, paired Markdown fences and balanced Persian RTL wrappers were checked. No scripts or Mermaid initialization directives were embedded.

All 28 internal file-link occurrences in the four new guides were checked against the inspected repository paths and the new files in this change. Numbered source references in both stack guides had matching definitions. Fourteen official documentation sources and GitHub's Mermaid guidance were consulted through web access. This was capability verification, not a full dependency/security audit.

Local Git blob identities for the new guide sources:

| File | Git blob SHA |
|---|---|
| `docs/en/DIAGRAMS.md` | `2f3338cc6cb920f07f310618f9cf7d02c8f0548b` |
| `docs/en/TECH_STACK.md` | `cd2d353f62787dcbc912b216fe64e4ebcc37c3c6` |
| `docs/fa/DIAGRAMS.md` | `c299712f88507659acdb213be0c61e458eb79fa4` |
| `docs/fa/TECH_STACK.md` | `cbb779064713363a454b0516da6e5fd80a4c5392` |

### Preservation and limitations

The original master-prompt blob is `d6420b4436907c8a9daa5599dc8e7398b540b280`; that file is not included in any write for this change. The original requirement traceability and Phase 0 approval gate remain in effect. Prior [validation notes](VALIDATION.md) describe the earlier publication separately.

No Mermaid parser/CLI or browser rendering test ran: Mermaid was not installed in the working container, and its direct outbound GitHub access failed. Structural equivalence and balanced fences do not prove that GitHub renders every diagram correctly or that Persian labels fit well. Final visual inspection in GitHub remains outstanding. The existing whole-repository checker, application tests, CPU benchmarks, real-device tests and deployment tests were not run for this update. No claim is made that CI, branch protection or runtime controls have been configured.

The README overview diagrams are additional to the fourteen atlas diagrams. The local guide-link and diagram-parity counts above apply only to the four new guide files, not to every file in the repository.

## فارسی

دامنهٔ کار فقط مستندات است: راهنمای نمودار و فناوری به فارسی و انگلیسی، پیوندهای README و فهرست‌ها و ثبت وضعیت پروژه. دسترسی به میزبان، نصب، تماس عملیاتی، اجرای مدل یا تغییر وابستگی اجرایی انجام نشده است.

### بررسی‌های انجام‌شده روی چهار راهنمای جدید

ابزار محلی Python بلوک‌های Mermaid را استخراج کرد: هفت نمودار در هر زبان و چهارده نمودار در مجموع. پس از کنار گذاشتن برچسب‌های ترجمه‌شده، نوع نمودار و ترتیب ارتباط‌ها و گذارها در دو نسخه یکسان بود. نمودار مفهومی داده عیناً یکسان بود. متن UTF-8، پایان سطر، جفت بودن حصارهای Markdown و باز و بسته شدن کادرهای RTL بررسی شدند. اسکریپت یا دستور مقداردهی ویژهٔ Mermaid در متن قرار نگرفت.

هر ۲۸ مورد پیوند داخلیِ چهار راهنما با مسیرهای مشاهده‌شدهٔ مخزن و فایل‌های تازه تطبیق داده شد. ارجاع‌های شماره‌دار هر دو راهنمای فناوری تعریف متناظر داشتند. چهارده منبع رسمی ابزارها و راهنمای Mermaid در GitHub از طریق وب بررسی شدند. این بررسی دربارهٔ قابلیت ابزار بود، نه ممیزی کامل وابستگی و امنیت. هش فایل‌های محلی در جدول بالا ثبت شده است.

### حفظ منبع و محدودیت‌ها

فایل پرامپت با هش درج‌شده در بالا در هیچ‌یک از تغییرات نوشته نمی‌شود. ردیابی نیازهای اولیه و الزام تأیید مرحلهٔ صفر برقرار است. [گزارش قبلی](VALIDATION.md) مربوط به انتشار پیشین است.

آزمون تجزیه‌گر یا نمایش مرورگری Mermaid اجرا نشد؛ ابزار در محیط محلی نصب نبود و ارتباط خروجی مستقیم آن محیط با GitHub برقرار نشد. یکسان بودن ساختار و کامل بودن بلوک‌ها، نمایش بی‌خطا یا خوانایی برچسب فارسی را ثابت نمی‌کند. بازبینی بصری در GitHub همچنان انجام‌نشده است. ابزار بررسی کل مخزن، آزمون برنامه، کارایی CPU، اتصال واقعی و استقرار برای این تغییر اجرا نشده‌اند. تنظیم بودن CI، حفاظت شاخه یا کنترل‌های اجرایی ادعا نمی‌شود.

نمودارهای خلاصهٔ README علاوه بر چهارده نمودار مجموعه‌اند. تعداد پیوند و تطبیق ساختارِ گزارش‌شده فقط به چهار راهنمای جدید مربوط است، نه تمام فایل‌های مخزن.
