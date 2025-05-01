function assertJquery(func) {
    if (typeof jQuery == 'undefined') {
        var script = document.createElement('script');
        script.src = 'https://code.jquery.com/jquery-3.7.1.min.js';
        script.type = 'text/javascript';
        script.onload = func;
        document.getElementsByTagName('head')[0].appendChild(script);
    } else {
        func();
    }
}

function initPlayer(scenarioRaw) {
    if (!scenarioRaw) {
        console.warn('No scenario found in localStorage.');
        return;
    }

    var scenarioData = JSON.parse(scenarioRaw);

    if (!Array.isArray(scenarioData)) {
        console.error('Invalid scenario format.');
        return;
    }

    // 이벤트 하나씩 실행
    var startTime = performance.now();

    function runStep(index) {
        if (index >= scenarioData.length) {
            console.log('Playback completed.');
            return;
        }

        var step = scenarioData[index];
        var currentTime = performance.now();
        var delay = (step.timestamp * 1000) - (currentTime - startTime);

        if (delay < 0) delay = 0;

        setTimeout(function() {
            handleStep(step);
            runStep(index + 1);
        }, delay);
    }

    function handleStep(step) {
        var $el = $(step.selector);
        if (!$el.length) {
            console.warn('Element not found for selector:', step.selector);
            return;
        }

        switch (step.type) {
            case 'click':
                $el.trigger('click');
                break;
            case 'input':
                $el.val(step.value).trigger('input');
                break;
            default:
                console.warn('Unknown step type:', step.type);
        }
    }

    runStep(0); // 첫번째 스텝부터 시작
}

(function() {
    assertJquery(function() {
        var scenarioRaw = localStorage.getItem('testtool_logs');
        initPlayer(scenarioRaw);
    });
})();
  