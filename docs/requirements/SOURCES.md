# Source and documentation provenance / مبنای مستندات

## English

Primary source: the supplied `NEXTOPS_MASTER_PROMPT.md`, version 2.0, prepared 2026-09-19. It is stored as [the master specification](NEXTOPS_MASTER_PROMPT.md). Its existing Appendix A preserves the original Persian `nextops.txt` specification, including all 51 numbered sections and the eleven integration families.

The owner's explicit deployment additions are GitHub, one G10-class host with approximately 90 CPU units and 1 TB RAM, sufficient storage, no GPU and all AI on local CPUs. Hardware details remain reported rather than verified. The current instruction authorizes bilingual repository documentation; the prompt is not newly translated.

The English/Persian guides reorganize the supplied requirements into readable engineering documentation. They preserve the master prompt's explicit revisions where its appendix conflicts: early security/inference, local-only providers, phased vertical slices, PostgreSQL-first persistence, non-bypassable safety, evidence-qualified RCA and single-host limitations. ADRs are proposed decisions, not proof of owner sign-off. The documentation checker, navigation and review templates are repository-support additions, not application implementation.

References embedded in the master prompt are implementation starting points. This documentation task does not claim a new external verification of vendor versions, model performance or library compatibility. Recheck official versioned sources when implementation begins. Do not silently upgrade a recommendation into a measured fact.

## فارسی

منبع اصلی، فایل دریافت‌شدهٔ `NEXTOPS_MASTER_PROMPT.md` نسخهٔ ۲.۰ با تاریخ آماده‌سازی ۱۹ سپتامبر ۲۰۲۶ است که در [مشخصات اصلی](NEXTOPS_MASTER_PROMPT.md) نگهداری می‌شود. پیوست A موجود در آن متن اولیهٔ فارسی `nextops.txt` را با ۵۱ بخش شماره‌دار و یازده خانوادهٔ اتصال حفظ می‌کند.

افزودهٔ صریح مالک شامل GitHub، یک میزبان G10 با حدود ۹۰ واحد CPU و یک ترابایت RAM، فضای کافی، نبود GPU و اجرای همهٔ هوش مصنوعی روی CPU محلی است. مشخصات سخت‌افزار اعلام‌شده‌اند، نه تأییدشده. درخواست فعلی اجازهٔ مستندسازی دوزبانهٔ مخزن را می‌دهد و پرامپت ترجمهٔ تازه ندارد.

راهنماها نیازها را به مستندات مهندسی خوانا تبدیل می‌کنند. در تعارض با پیوست، اصلاحات صریح پرامپت حفظ می‌شوند: امنیت و مدل از ابتدا، ارائه‌دهندهٔ صرفاً محلی، تحویل جریان کامل، PostgreSQL اولیه، کنترل غیرقابل‌دورزدن، علت‌یابی متکی بر شاهد و محدودیت تک‌میزبان. ADR پیشنهاد تصمیم است، نه اثبات تأیید مالک. ابزار بررسی، مسیریابی مستندات و قالب بازبینی افزودهٔ پشتیبان مخزن‌اند، نه پیاده‌سازی برنامه.

ارجاع‌های داخل پرامپت نقطهٔ آغاز بررسی هنگام پیاده‌سازی‌اند. این کار ادعای بررسی تازهٔ نسخهٔ فروشنده، سرعت مدل یا سازگاری کتابخانه ندارد. منابع رسمی نسخه‌دار هنگام ساخت دوباره بررسی شوند. پیشنهاد بی‌صدا به واقعیت اندازه‌گیری‌شده تبدیل نشود.
