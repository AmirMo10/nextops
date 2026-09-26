# Prompt version history / تاریخچهٔ نسخه‌های پرامپت

## Owner clarification of the recovery claim — 2026-09-26

The owner clarified that the verification was restoration from an ESXi VM snapshot only. It does
not evidence independent PostgreSQL backup, WAL/PITR, isolated database restore, key/artifact
recovery or survival of loss of the serving hypervisor/storage. The active non-recovery delivery
sequence is unchanged, and the full-production recovery gates remain unpassed.

مالک روشن کرد که آزمون انجام‌شده فقط بازیابی از snapshot ماشین ESXi بوده است. این آزمون شاهدِ
پشتیبان مستقلِ PostgreSQL، ‏WAL/PITR، بازیابی ایزولهٔ پایگاه، بازیابی کلید و فایل یا دوام در برابر
خرابی میزبان و ذخیره‌سازی نیست. ترتیب تحویل غیربازیابی تغییر نمی‌کند و معیارهای بازیابیِ پذیرش
کامل تولید همچنان پذیرفته نشده‌اند.

## Owner scope amendment — 2026-09-26

The owner reports daily ESXi snapshots of all four local servers and directs the team to complete
non-recovery work without treating independent recovery as the first active blocker. This later
instruction changes the current delivery sequence, not the historical v3.0/v2.0 text or the
meaning of a passed backup/restore test. Snapshot configuration and successful restoration have
not been verified. The checked-in recovery profile remains blocked, and full production acceptance
cannot be claimed under its existing contract. Other security, quality, offline and approval gates
are unchanged. The release manifest records the owner-directed scope explicitly.

مالک اعلام کرده است که از هر چهار سرور محلی هر روز در ESXi snapshot گرفته می‌شود و خواسته است کارهای
غیربازیابی، بدون قرار دادن مقصد مستقل بازیابی در ابتدای صف، ادامه یابند. این دستورِ جدید ترتیب
تحویل فعلی را تغییر می‌دهد، نه متن تاریخی نسخه‌های ۳ و ۲ یا معنای آزمون موفق پشتیبان و بازیابی را.
پیکربندی snapshot و بازیابی موفق آن مستقلاً تأیید نشده‌اند؛ پروفایل بازیابی همچنان مسدود است و
ادعای پذیرش کامل تولید مجاز نیست. سایر دروازه‌های کیفیت، امنیت، کارکرد آفلاین و تأیید انسانی
برقرارند. دامنهٔ جدید در مانیفست انتشار ثبت شده است.

## v3.0 — 2026-09-20

[Active prompt](NEXTOPS_MASTER_PROMPT.md) · [Preserved v2.0](archive/NEXTOPS_MASTER_PROMPT_v2.0.md) · [Source provenance](SOURCES.md)

### English

Owner authorization: update the prompt as needed after the hardware, datastore and deployment discussions. This is a documentation revision only; it does not approve provisioning or complete any implementation phase.

| Topic | Reconciled instruction |
|---|---|
| Repository | Use the existing `AmirMo10/nextops`; inspect its current work instead of assuming no repository exists. |
| Hardware evidence | Use 4 packages, 112 physical cores, 224 threads, 4 NUMA nodes and 1,442,743,631,872 bytes RAM; retain source and uncertainty labels. |
| Host/guest boundary | Preserve ESXi 8.0.3 build 24414501. Ubuntu Server 24.04 LTS is the proposed guest, not an ESXi replacement. |
| First milestone | Phase 1 finishes with a real offline local-CPU answer about authorized Zabbix status. Linux enrichment remains Phase 2. |
| Starting stages | 1A application/security; 1B local model; 1C restricted Zabbix evidence; 1D answer; 1E offline acceptance. |
| VM creation | App first, AI second, read-only connectors third; 8/24/4 vCPU, 32/128/8 GiB RAM, 200/500/80 GiB disk. |
| Initial totals | 3 NextOps VMs, 36 vCPU, 168 GiB RAM, 780 GiB VMDKs; not actual reservations or measured minimums. |
| Storage | Retain 3 TB project ceiling and DS-C-specific evidence; initial provisional VMDK-plus-swap subtotal 948 GiB; exact 25% DS-C free target 894.1875 GiB, conservatively about 900. |
| Offline behavior | Normal CPU-local generation online or offline, fresh login, cold start/reboot, local assets and protected key access; no external AI fallback. |
| Evidence and tests | Preserve status semantics, deterministic counts, source/time/scope reporting, ZBX-01–ZBX-08 and applicable OFF-01–OFF-10; all tests remain unrun until evidence is recorded. |
| Source preservation | Archive the complete previous prompt using its existing Git blob; keep the original Persian appendix intact and no new prompt translation. |
| Continuation | Resume the next unfinished authorized checkpoint; do not repeat supplied discovery or restart Phase 0 after it is actually approved and complete. |

The active prompt keeps the original 26 engineering sections and explicitly incorporates non-conflicting detailed v2 requirements. All 51 original sections and eleven integrations remain traceable; this update does not reduce their scope. Current v3 decisions override stale hardware, sequencing or cloud examples and older statements forbidding any prompt edit. Such immutability now applies to the archived v2 source.

Archive Git blob: `d6420b4436907c8a9daa5599dc8e7398b540b280`.
Archive SHA-256: `35d7f8be94145bacc53ca4447695abbcab6115b1a3812a087251ddc2850c54c4`.

Validation boundary: source/archive identity and Git changes can be checked independently of application tests. The documentation-only update performs no VM creation, host inspection, model download/run, benchmark, Zabbix call, patch installation, network shutdown, offline restart or restore test. It does not claim a full repository checkout/test run when unavailable.

### فارسی

مجوز مالک، به‌روزرسانی پرامپت پس از گفت‌وگو دربارهٔ سخت‌افزار، ذخیره‌سازی و ترتیب شروع است. این کار فقط بازنگری مستندات است؛ نه اجازهٔ ساخت ماشین و نه تکمیل مرحله‌ای از پیاده‌سازی.

نسخهٔ ۳، مخزن موجود، مشخصات ارسالیِ ۱۱۲ هسته و ۲۲۴ رشته و چهار گره، نسخهٔ ESXi و نقش Ubuntu به‌عنوان مهمان را مبنا قرار می‌دهد. اولین خروجی باید در پایان مرحلهٔ یک، پاسخ واقعی و مستند هوش مصنوعی محلی دربارهٔ Zabbix با اینترنت قطع باشد؛ بررسی تکمیلی Linux در مرحلهٔ دو باقی می‌ماند.

ترتیب ساخت، برنامه سپس AI و سپس اتصال فقط‌خواندنی است: به‌ترتیب ۸، ۲۴ و ۴ vCPU؛ حافظهٔ ۳۲، ۱۲۸ و ۸ GiB؛ دیسک ۲۰۰، ۵۰۰ و ۸۰ GiB. مجموع اولیه ۳ ماشین، ۳۶ vCPU، حافظهٔ ۱۶۸ GiB و دیسک ۷۸۰ GiB است. مراحل 1A تا 1E پایهٔ امنیت، مدل محلی، شواهد محدود Zabbix، پاسخ کاربردی و پذیرش آفلاین را پوشش می‌دهند.

سقف سه‌ترابایتی پروژه و محل پیشنهادی DS-C حفظ شده‌اند. با سهم موقت swap، جمع اولیه ۹۴۸ GiB است. هدف دقیق حاشیهٔ آزادِ ۲۵ درصد روی DS-C برابر ۸۹۴٫۱۸۷۵ GiB است که محافظه‌کارانه حدود ۹۰۰ در نظر گرفته می‌شود. این اعداد پیشنهاد و محاسبه‌اند؛ نه رزرو اعمال‌شده یا حداقل اندازه‌گیری‌شده.

تولید پاسخ همیشه محلی و مبتنی بر CPU است؛ ورود تازه، شروع از حالت متوقف، روشن شدن دوباره، فایل‌های رابط و دسترسی امن به کلیدها نباید اینترنت بخواهند. معیارهای ZBX و OFF، شمارش قطعی و نمایش منبع و زمان و دامنه برقرارند. آزمون بدون شاهد واقعی، قبول‌شده معرفی نمی‌شود.

ساختار ۲۶بخشی مهندسی حفظ شده و جزئیات بدون تعارضِ نسخهٔ ۲ همچنان الزامی‌اند. تمام ۵۱ بخش اولیه و یازده اتصال باقی می‌مانند. نسخهٔ کامل قبلی با همان شناسهٔ Git بالا در بایگانی نگهداری می‌شود؛ پیوست فارسی آن دست‌نخورده است و ترجمهٔ تازه‌ای از پرامپت تهیه نشده است. عبارت‌های قدیمی دربارهٔ ثابت ماندن پرامپت از این پس به همین نسخهٔ بایگانی‌شده اشاره دارند.

عامل باید از نخستین گام ناتمامِ دارای مجوز ادامه دهد؛ نه اطلاعات ارسال‌شده را دوباره بخواهد و نه مرحلهٔ صفرِ واقعاً تأیید و تکمیل‌شده را بی‌پایان تکرار کند. این تغییر هیچ VM، مدل اجرایی، تماس با Zabbix، آزمون کارایی، تغییر شبکه یا آزمون بازیابی ایجاد یا اجرا نمی‌کند. بررسی هویت منبع و تغییرات Git با آزمون محصول یکی نیست.

## v2.0 — prepared 2026-09-19

The prior complete engineering prompt and its original Persian appendix are preserved in the linked archive. Later owner clarifications now live in v3.0 and the dated evidence records.

نسخهٔ کامل پیشین و پیوست فارسی اولیه در بایگانی بالا حفظ شده‌اند. توضیحات بعدی مالک در نسخهٔ ۳.۰ و رکوردهای تاریخ‌دار شواهد اعمال شده‌اند.
