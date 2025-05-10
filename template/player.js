(function() {
    console.log('player inject!');

    // 쿠키 유틸 함수들
    function setCookie(name, value, options = {}) {
        options = {
            path: '/',
            'max-age': 3600, // 기본 1시간
            ...options
        };

        let updatedCookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}`;
        for (let [key, val] of Object.entries(options)) {
            updatedCookie += `; ${key}`;
            if (val !== true) {
                updatedCookie += `=${val}`;
            }
        }

        document.cookie = updatedCookie;
    }

    function getCookie(name) {
        const matches = document.cookie.match(
            new RegExp(`(?:^|; )${encodeURIComponent(name)}=([^;]*)`)
        );
        return matches ? decodeURIComponent(matches[1]) : undefined;
    }

    function deleteCookie(name, options = {}) {
        setCookie(name, '', {
            ...options,
            'max-age': 0
        });
    }

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
    window.player.setCookie = setCookie;
    window.player.getCookie = getCookie;
    window.player.deleteCookie = deleteCookie;

    window.player.start = (log, scenarioName, playId) => {
        setCookie('X-PLAY-ID', playId);
        setCookie('X-SCENARIO-ID', scenarioName ?? '');
        replay(log);
    };
    window.player.stop = () => {
        deleteCookie('X-PLAY-ID');
        deleteCookie('X-SCENARIO-ID');
    };
})();
