# scheduler.py
# إدارة التحديثات الدورية للبوت (مواقع الأفلام العربية والمترجمة)

import schedule
import time
from arabic_cinema_sites import get_free_arabic_sites

# =========================
# دالة تحديث المواقع
# =========================
def update_free_arabic_sites():
    """
    تحديث قائمة مواقع الأفلام والمسلسلات العربية والمترجمة.
    يمكن تعديل هذه الدالة لاحقًا لتخزين النتائج في قاعدة بيانات.
    """
    sites = get_free_arabic_sites()
    
    # مثال: هنا حفظها في قاعدة بيانات أو مجرد طباعة للعينة
    print("🚀 تحديث المواقع العربية بدأ...")
    for site in sites:
        print(f"✅ {site['title']} - {site['link']} [{site['type']}]")
    print("🎉 تحديث المواقع العربية انتهى!\n")


# =========================
# جدول التحديثات الدورية
# =========================
def schedule_updates():
    """
    إعداد الجدول الزمني لتحديث المواقع بشكل دوري.
    - يمكن تعديل الوقت حسب الحاجة (مثلاً: كل يوم الساعة 12:00)
    """
    # تحديث يومي
    schedule.every().day.at("12:00").do(update_free_arabic_sites)

    # تحديث كل ساعة (اختياري)
    # schedule.every(1).hours.do(update_free_arabic_sites)

    print("🕒 بدء تشغيل جدول التحديثات الدورية...")
    while True:
        schedule.run_pending()
        time.sleep(60)


# =========================
# نقطة البداية
# =========================
if __name__ == "__main__":
    update_free_arabic_sites()  # تحديث أولي عند تشغيل السكربت
    schedule_updates()           # تشغيل الجدول الدوري
