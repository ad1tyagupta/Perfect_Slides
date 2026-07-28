/* ===========================================================================
   DECK CONTROLLER — include this entire file in every HTML deck.

   Navigation, stage scaling, presenting mode, presenter view, and the
   behaviours shared by every component (counters, flips, tabs).
   No dependencies.
   =========================================================================== */

class Deck {
    constructor() {
        this.slides = [...document.querySelectorAll('.slide')];
        this.stage = document.getElementById('deckStage');
        this.progress = document.querySelector('.deck-progress');
        this.current = 0;
        this.presenterWindow = null;

        this.scale();
        addEventListener('resize', () => this.scale());

        this.bindKeys();
        this.bindTouch();
        this.bindWheel();
        this.bindChrome();
        this.bindFullscreen();

        // Deep link: deck.html#7 opens on slide 7.
        const fromHash = parseInt(location.hash.slice(1), 10);
        this.show(Number.isInteger(fromHash) ? fromHash - 1 : 0);
    }

    /* --- Scale the 1920x1080 stage to fit the window, letterboxing ------- */
    scale() {
        const f = Math.min(innerWidth / 1920, innerHeight / 1080);
        const x = (innerWidth - 1920 * f) / 2;
        const y = (innerHeight - 1080 * f) / 2;
        this.stage.style.transform = `translate(${x}px, ${y}px) scale(${f})`;
    }

    /* --- Slide switching ------------------------------------------------- */
    show(i) {
        this.current = Math.max(0, Math.min(i, this.slides.length - 1));

        this.slides.forEach((s, n) => {
            const on = n === this.current;
            s.classList.toggle('active', on);
            s.classList.toggle('visible', on);
            s.setAttribute('aria-hidden', String(!on));
        });

        const counter = document.querySelector('.deck-controls .count');
        if (counter) counter.textContent = `${this.current + 1} / ${this.slides.length}`;

        if (this.progress) {
            this.progress.style.width = ((this.current + 1) / this.slides.length * 100) + '%';
        }

        history.replaceState(null, '', '#' + (this.current + 1));

        this.runCounters(this.slides[this.current]);
        this.replayAnimations(this.slides[this.current]);
        this.pushToPresenter();
    }

    next() { this.show(this.current + 1); }
    prev() { this.show(this.current - 1); }

    /* --- Numbers that count up on arrival --------------------------------
       <span data-count="53.6" data-dec="1">0</span>
       data-dec  decimal places, default 0
       data-sep  set to "1" for thousands separators
       --------------------------------------------------------------------- */
    runCounters(slide) {
        slide.querySelectorAll('[data-count]').forEach(el => {
            const target = parseFloat(el.dataset.count);
            const dec = parseInt(el.dataset.dec || 0, 10);
            const sep = el.dataset.sep === '1';
            const dur = parseInt(el.dataset.dur || 1300, 10);
            const t0 = performance.now();

            const tick = t => {
                const p = Math.min((t - t0) / dur, 1);
                const eased = 1 - Math.pow(1 - p, 3);
                const v = (target * eased).toFixed(dec);
                el.textContent = sep ? Number(v).toLocaleString(undefined, {
                    minimumFractionDigits: dec, maximumFractionDigits: dec
                }) : v;
                if (p < 1) requestAnimationFrame(tick);
            };

            requestAnimationFrame(tick);
        });
    }

    /* --- Restart keyframe animations when a slide is revisited ----------- */
    replayAnimations(slide) {
        slide.querySelectorAll('[data-replay]').forEach(el => {
            el.style.animation = 'none';
            void el.offsetWidth;          // force reflow
            el.style.animation = '';
        });
    }

    /* --- Input ------------------------------------------------------------ */
    bindKeys() {
        addEventListener('keydown', e => {
            if (e.target.isContentEditable || /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) return;

            if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(e.key)) {
                e.preventDefault(); this.next();
            } else if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key)) {
                e.preventDefault(); this.prev();
            } else if (e.key === 'Home') {
                e.preventDefault(); this.show(0);
            } else if (e.key === 'End') {
                e.preventDefault(); this.show(this.slides.length - 1);
            } else if (e.key === 'f' || e.key === 'F') {
                e.preventDefault(); this.toggleFullscreen();
            } else if (e.key === 'p' || e.key === 'P') {
                e.preventDefault(); this.openPresenter();
            }
        });
    }

    bindTouch() {
        let x0 = null, y0 = null;

        addEventListener('touchstart', e => {
            x0 = e.touches[0].clientX;
            y0 = e.touches[0].clientY;
        }, { passive: true });

        addEventListener('touchend', e => {
            if (x0 === null) return;
            const dx = e.changedTouches[0].clientX - x0;
            const dy = e.changedTouches[0].clientY - y0;
            // Horizontal intent only, so vertical scrolling inside a slide still works.
            if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
                dx < 0 ? this.next() : this.prev();
            }
            x0 = y0 = null;
        }, { passive: true });
    }

    bindWheel() {
        let lock = false;
        addEventListener('wheel', e => {
            if (lock) return;
            if (Math.abs(e.deltaY) < 24 && Math.abs(e.deltaX) < 24) return;
            lock = true;
            (e.deltaY || e.deltaX) > 0 ? this.next() : this.prev();
            setTimeout(() => lock = false, 650);
        }, { passive: true });
    }

    bindChrome() {
        const prev = document.querySelector('[data-nav="prev"]');
        const next = document.querySelector('[data-nav="next"]');
        const full = document.querySelector('[data-nav="fullscreen"]');
        if (prev) prev.onclick = () => this.prev();
        if (next) next.onclick = () => this.next();
        if (full) full.onclick = () => this.toggleFullscreen();
    }

    /* --- Presenting mode: fullscreen, chrome hides after 2.5s idle -------- */
    bindFullscreen() {
        let timer = null;

        const poke = () => {
            document.body.classList.add('show-chrome');
            clearTimeout(timer);
            timer = setTimeout(() => document.body.classList.remove('show-chrome'), 2500);
        };

        const onChange = () => {
            const on = !!(document.fullscreenElement || document.webkitFullscreenElement);
            document.body.classList.toggle('presenting', on);
            this.scale();
            on ? poke() : document.body.classList.remove('show-chrome');
        };

        document.addEventListener('fullscreenchange', onChange);
        document.addEventListener('webkitfullscreenchange', onChange);
        addEventListener('mousemove', () => {
            if (document.body.classList.contains('presenting')) poke();
        });
    }

    toggleFullscreen() {
        const el = document.documentElement;
        const isFull = document.fullscreenElement || document.webkitFullscreenElement;
        try {
            const fn = isFull
                ? (document.exitFullscreen || document.webkitExitFullscreen)
                : (el.requestFullscreen || el.webkitRequestFullscreen);
            const p = fn && fn.call(isFull ? document : el);
            if (p && p.catch) p.catch(() => {});
        } catch (_) { /* fullscreen unavailable, not fatal */ }
    }

    /* --- Presenter view: notes, next slide and a timer in a second window -
       Press P. Put it on the laptop screen, the deck on the projector.
       --------------------------------------------------------------------- */
    openPresenter() {
        if (this.presenterWindow && !this.presenterWindow.closed) {
            this.presenterWindow.focus();
            return;
        }

        this.presenterWindow = open('', 'presenter', 'width=900,height=620');
        if (!this.presenterWindow) return;   // popup blocked

        this.presenterWindow.document.write(`<!DOCTYPE html><meta charset="utf-8">
<title>Presenter view</title>
<style>
  body{margin:0;padding:28px;background:#111;color:#eee;
       font:16px/1.55 system-ui,sans-serif;display:grid;gap:22px;
       grid-template-rows:auto auto 1fr}
  .row{display:flex;justify-content:space-between;align-items:baseline;
       border-bottom:1px solid #333;padding-bottom:12px}
  .pos{font-size:15px;color:#888;letter-spacing:.06em}
  .timer{font-size:34px;font-variant-numeric:tabular-nums}
  h2{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:#888;
     font-weight:600;margin-bottom:8px}
  .notes{font-size:19px;white-space:pre-wrap}
  .next{color:#aaa;font-size:17px}
</style>
<div class="row"><span class="pos" id="pos"></span><span class="timer" id="timer">00:00</span></div>
<div><h2>Notes</h2><div class="notes" id="notes"></div></div>
<div><h2>Up next</h2><div class="next" id="next"></div></div>
<script>
  const t0 = Date.now();
  setInterval(() => {
    const s = Math.floor((Date.now() - t0) / 1000);
    document.getElementById('timer').textContent =
      String(Math.floor(s / 60)).padStart(2,'0') + ':' + String(s % 60).padStart(2,'0');
  }, 1000);
<\/script>`);
        this.presenterWindow.document.close();
        this.pushToPresenter();
    }

    pushToPresenter() {
        const w = this.presenterWindow;
        if (!w || w.closed || !w.document.getElementById('pos')) return;

        const notesEl = this.slides[this.current].querySelector('.speaker-notes');
        const nextSlide = this.slides[this.current + 1];
        const nextHead = nextSlide && nextSlide.querySelector('h1, h2, .headline');

        w.document.getElementById('pos').textContent =
            `Slide ${this.current + 1} of ${this.slides.length}`;
        w.document.getElementById('notes').textContent =
            notesEl ? notesEl.textContent.trim() : 'No notes for this slide.';
        w.document.getElementById('next').textContent =
            nextHead ? nextHead.textContent.trim() : 'End of deck.';
    }
}

/* ===========================================================================
   SHARED COMPONENT BEHAVIOUR
   Markup conventions live in references/components/interactive.md
   =========================================================================== */

/* Flip cards: <div class="flip"><div class="flip-inner">…</div></div> */
function bindFlipCards() {
    document.querySelectorAll('.flip').forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');

        const toggle = () => card.classList.toggle('flipped');
        card.addEventListener('click', toggle);
        card.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
        });
    });
}

/* Tab switchers: buttons carry data-tab="x", panels carry data-panel="x".
   Scoped per .tab-group so several can coexist on one slide. */
function bindTabs() {
    document.querySelectorAll('.tab-group').forEach(group => {
        const tabs = [...group.querySelectorAll('[data-tab]')];
        const panels = [...group.querySelectorAll('[data-panel]')];

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => {
                    const on = t === tab;
                    t.classList.toggle('on', on);
                    t.setAttribute('aria-selected', String(on));
                });
                panels.forEach(p => p.classList.toggle('on', p.dataset.panel === tab.dataset.tab));
            });
        });
    });
}

/* Charts with hoverable segments. The centre readout swaps to the hovered
   segment's value and returns to the default on leave. */
function bindChartHovers() {
    document.querySelectorAll('[data-chart-hover]').forEach(chart => {
        const big = chart.querySelector('[data-readout-value]');
        const sub = chart.querySelector('[data-readout-label]');
        if (!big || !sub) return;

        const rest = { big: big.innerHTML, sub: sub.innerHTML };

        chart.querySelectorAll('[data-value]').forEach(seg => {
            seg.addEventListener('mouseenter', () => {
                chart.classList.add('hovering');
                big.textContent = seg.dataset.value;
                sub.textContent = seg.dataset.label || '';
            });
            seg.addEventListener('mouseleave', () => {
                chart.classList.remove('hovering');
                big.innerHTML = rest.big;
                sub.innerHTML = rest.sub;
            });
        });
    });
}

/* Carousels: <div class="carousel" data-carousel> with [data-carousel-item],
   [data-carousel-prev], [data-carousel-next], [data-carousel-dots] */
function bindCarousels() {
    document.querySelectorAll('[data-carousel]').forEach(car => {
        const items = [...car.querySelectorAll('[data-carousel-item]')];
        const dots = car.querySelector('[data-carousel-dots]');
        if (!items.length) return;
        let i = 0;

        if (dots && !dots.children.length) {
            items.forEach(() => dots.appendChild(document.createElement('i')));
        }

        const render = () => {
            items.forEach((el, n) => el.classList.toggle('on', n === i));
            if (dots) [...dots.children].forEach((d, n) => d.classList.toggle('on', n === i));
        };

        const go = step => { i = (i + step + items.length) % items.length; render(); };

        const prev = car.querySelector('[data-carousel-prev]');
        const next = car.querySelector('[data-carousel-next]');
        if (prev) prev.onclick = () => go(-1);
        if (next) next.onclick = () => go(1);

        render();
    });
}

/* ===========================================================================
   INLINE EDITING

   Press E, or hover the top-left corner, to edit text directly in the deck.
   Changes save to this browser automatically. "Save a copy" downloads an HTML
   file with the edits baked in.

   Purpose: fixing a typo or rewording a headline should not cost a round trip
   back to the agent.
   =========================================================================== */

class Editor {
    constructor(deck) {
        this.deck = deck;
        this.active = false;
        this.key = 'deck-edits:' + location.pathname;

        this.toggle = document.getElementById('editToggle');
        this.hotzone = document.querySelector('.edit-hotzone');

        this.index();
        this.restore();
        this.bind();
        this.announce();
    }

    /* The pencil is invisible until you hover an unmarked corner, which means
       nobody discovers editing exists. Show it briefly on load, once, with a
       dismissible hint. */
    announce() {
        if (!this.toggle) return;
        this.toggle.classList.add('show');
        setTimeout(() => { if (!this.active) this.toggle.classList.remove('show'); }, 4000);

        let seen = false;
        try { seen = localStorage.getItem(this.key + ':hinted') === '1'; } catch (_) {}
        if (seen) return;

        const hint = document.createElement('div');
        hint.className = 'edit-hint';
        hint.innerHTML = '<b>E</b> to edit any text on this deck';
        document.body.appendChild(hint);

        const dismiss = () => {
            hint.classList.add('gone');
            setTimeout(() => hint.remove(), 400);
            try { localStorage.setItem(this.key + ':hinted', '1'); } catch (_) {}
        };
        hint.addEventListener('click', dismiss);
        setTimeout(dismiss, 6000);
    }

    /* Stable ids so saved edits survive a reload. Index within the slide, so
       adding a slide later does not shift everything.

       A field is an element whose children are only inline formatting. Headlines
       routinely carry <em> or <b> for emphasis, and excluding them would make
       the most important text on the deck the only text you cannot edit. */
    index() {
        const SELECTOR = 'h1,h2,h3,h4,p,li,blockquote,td,th,figcaption,div,span';
        const INLINE = new Set(['EM', 'B', 'STRONG', 'I', 'U', 'SMALL', 'SPAN',
                                'BR', 'SUB', 'SUP', 'MARK', 'CODE', 'ABBR']);
        this.fields = [];

        const inlineOnly = el =>
            [...el.children].every(c => INLINE.has(c.tagName) && inlineOnly(c));

        this.deck.slides.forEach((slide, s) => {
            let n = 0;
            slide.querySelectorAll(SELECTOR).forEach(el => {
                if (!(el.textContent || '').trim()) return;
                if (el.closest('.speaker-notes, .deck-controls')) return;
                if (el.querySelector('[data-count]') || el.hasAttribute('data-count')) return;
                if (!inlineOnly(el)) return;                    // has block children
                if (el.closest('[data-edit-id]')) return;       // already inside a field
                el.dataset.editId = `s${s}-f${n++}`;
                el.dataset.editRich = el.children.length ? '1' : '';
                this.fields.push(el);
            });
        });
    }

    bind() {
        if (this.toggle) this.toggle.addEventListener('click', () => this.flip());

        // Hover reveal needs JS with a grace period. A CSS sibling selector
        // fails here: pointer-events:none on the button breaks the hover chain
        // the moment the cursor leaves the hotzone heading for the button.
        if (this.hotzone && this.toggle) {
            let hideTimer = null;
            const show = () => { clearTimeout(hideTimer); this.toggle.classList.add('show'); };
            const hide = () => {
                hideTimer = setTimeout(() => {
                    if (!this.active) this.toggle.classList.remove('show');
                }, 400);
            };
            this.hotzone.addEventListener('mouseenter', show);
            this.hotzone.addEventListener('mouseleave', hide);
            this.toggle.addEventListener('mouseenter', show);
            this.toggle.addEventListener('mouseleave', hide);
        }

        addEventListener('keydown', e => {
            if ((e.key === 'e' || e.key === 'E') && !e.target.isContentEditable) {
                e.preventDefault();
                this.flip();
            }
            if (e.key === 'Escape' && this.active) this.flip();
            if (this.active && (e.metaKey || e.ctrlKey) && e.key === 's') {
                e.preventDefault();
                this.download();
            }
        });
    }

    flip() { this.active ? this.stop() : this.start(); }

    start() {
        this.active = true;
        document.body.classList.add('editing');
        if (this.toggle) { this.toggle.classList.add('show', 'active'); this.toggle.textContent = '✕'; }

        this.fields.forEach(el => {
            // Rich fields keep their <em>/<b>; plain ones are locked to text so
            // a paste cannot inject markup into the slide.
            el.setAttribute('contenteditable', el.dataset.editRich ? 'true' : 'plaintext-only');
            el.addEventListener('input', this.save);
        });

        this.bar = document.createElement('div');
        this.bar.className = 'edit-bar';
        this.bar.innerHTML = '<span>Click any text to edit</span>' +
            '<button data-edit="save">Save a copy</button>' +
            '<button data-edit="reset">Undo all</button>' +
            '<button data-edit="done">Done</button>';
        document.body.appendChild(this.bar);

        this.bar.addEventListener('click', e => {
            const what = e.target.dataset.edit;
            if (what === 'save') this.download();
            if (what === 'reset') this.reset();
            if (what === 'done') this.stop();
        });
    }

    stop() {
        this.active = false;
        document.body.classList.remove('editing');
        if (this.toggle) { this.toggle.classList.remove('active'); this.toggle.textContent = '✎'; }

        this.fields.forEach(el => {
            el.removeAttribute('contenteditable');
            el.removeEventListener('input', this.save);
        });

        if (this.bar) { this.bar.remove(); this.bar = null; }
    }

    save = () => {
        const edits = {};
        this.fields.forEach(el => {
            edits[el.dataset.editId] = el.dataset.editRich ? el.innerHTML : el.textContent;
        });
        try {
            localStorage.setItem(this.key, JSON.stringify(edits));
        } catch (_) {
            // Private browsing, or storage full. Editing still works for this
            // session; "Save a copy" is the way out.
            this.warnNoStorage();
        }
    };

    warnNoStorage() {
        if (this.warned || !this.bar) return;
        this.warned = true;
        this.bar.querySelector('span').textContent =
            'This browser will not save edits. Use "Save a copy" before closing.';
    }

    restore() {
        let edits;
        try { edits = JSON.parse(localStorage.getItem(this.key) || '{}'); } catch (_) { return; }
        this.fields.forEach(el => {
            const saved = edits[el.dataset.editId];
            if (saved === undefined) return;
            if (el.dataset.editRich) {
                if (saved !== el.innerHTML) el.innerHTML = saved;
            } else if (saved !== el.textContent) {
                el.textContent = saved;
            }
        });
    }

    reset() {
        try { localStorage.removeItem(this.key); } catch (_) {}
        location.reload();
    }

    /* Writes out the live DOM, minus editing chrome, so the downloaded file is
       a clean deck with the edits baked in. */
    download() {
        const clone = document.documentElement.cloneNode(true);
        clone.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
        clone.querySelectorAll('.edit-bar').forEach(el => el.remove());
        clone.querySelectorAll('.slide').forEach(el => {
            el.classList.remove('visible');
            el.style.visibility = '';
        });
        const first = clone.querySelector('.slide');
        if (first) first.classList.add('active');

        const html = '<!DOCTYPE html>\n' + clone.outerHTML;
        const url = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
        const a = document.createElement('a');
        const name = (location.pathname.split('/').pop() || 'deck.html').replace(/\.html?$/, '');
        a.href = url;
        a.download = `${name}-edited.html`;
        a.click();
        URL.revokeObjectURL(url);
    }
}

/* --- Boot ---------------------------------------------------------------- */
const deck = new Deck();
bindFlipCards();
bindTabs();
bindChartHovers();
bindCarousels();
const editor = new Editor(deck);
