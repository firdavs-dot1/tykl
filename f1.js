async function sendPageHTMLToBot() {
    // Testlar qismini olishga harakat qilish
    const testElements = document.querySelectorAll('.test-list'); // Saytning testlar klassiga moslashtiring
    let testContent = '';
    testElements.forEach(test => testContent += test.outerHTML);
    const html = testContent || document.documentElement.outerHTML; // Agar test topilmasa, butun sahifa
    try {
        const response = await fetch("https://YOUR_RENDER_URL/upload-html", { // YOUR_RENDER_URL ni Render.com URL bilan almashtiring
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ html })
        });
        if (response.ok) {
            const div = document.createElement("div");
            div.textContent = "Skript yuklandi! Test ma'lumotlari botga yuborildi.";
            div.style.cssText = "position:fixed;bottom:10px;right:10px;background-color:#007bff;color:white;padding:8px 14px;border-radius:6px;font-family:sans-serif;font-size:14px;z-index:9999;box-shadow:0 0 6px rgba(0,0,0,0.2);";
            document.body.appendChild(div);
            setTimeout(() => div.remove(), 3000);
        }
    } catch (err) {
        console.error("❌ HTML yuborishda xatolik:", err);
    }
}

// Skript yuklanganda avtomatik ishga tushadi
sendPageHTMLToBot();
