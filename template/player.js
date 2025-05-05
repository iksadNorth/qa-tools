(function() {
    console.log('player inject!');

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
    
    async function replay(log) {
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

    // 전역 변수 등록
    window.player = {};

    window.player.injected = true;
    window.player.start = replay;
    window.player.stop = () => {};
})();
