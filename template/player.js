(function() {
    function waitForElementAsync(selector) {
        return new Promise(resolve => {
            const existing = document.querySelector(selector);
            if (existing) return resolve(existing);
    
            const observer = new MutationObserver(() => {
                const el = document.querySelector(selector);
                if (!el) return ;
                observer.disconnect();
                resolve(el);
            });
    
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        });
    }
    
    window.run = async function(log) {
        switch (log.type) {
            case 'click': {
                const el = await waitForElementAsync(log.selector);
                el.click();
                break;
            }
            case 'input': {
                const el = await waitForElementAsync(log.selector);
                el.value = log.value;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                break;
            }
            case 'navigate': {
                if (location.href !== log.to) {
                    location.href = log.to;
                }
                break;
            }
        }
    }
})();
