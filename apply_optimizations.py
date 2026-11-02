# -*- coding: utf-8 -*-
import os, re

# =========================================================================
# 1. Update index.html with Real-Time Search & Filter Toolbar
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

filter_css = '''
    /* Real-time Search & Filter Toolbar */
    .filter-toolbar {
      background: rgba(11, 18, 38, 0.72);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(56, 189, 248, 0.28);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin-bottom: 22px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .filter-search-row {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }
    .search-input-box {
      flex: 1;
      position: relative;
      min-width: 260px;
    }
    .search-input-box input {
      width: 100%;
      background: rgba(5, 9, 22, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 8px;
      color: #fff;
      padding: 10px 14px 10px 38px;
      font-size: 13.5px;
      outline: none;
      transition: all 0.2s;
    }
    .search-input-box input:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
    }
    .search-icon-svg {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      width: 16px;
      height: 16px;
      stroke: var(--text-dim);
      pointer-events: none;
    }
    .filter-count-badge {
      font-size: 12px;
      color: var(--text-dim);
      white-space: nowrap;
    }
    .filter-count-badge strong {
      color: var(--primary);
    }
    .filter-tags-row {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .tag-filter-pill {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 16px;
      padding: 5px 12px;
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }
    .tag-filter-pill:hover {
      background: rgba(56, 189, 248, 0.15);
      color: #fff;
      border-color: #38bdf8;
    }
    .tag-filter-pill.active {
      background: #0284c7;
      color: #fff;
      border-color: #0284c7;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4);
      font-weight: 700;
    }
    .no-results-box {
      text-align: center;
      padding: 40px 20px;
      background: rgba(11, 18, 38, 0.6);
      border: 1px dashed rgba(56, 189, 248, 0.3);
      border-radius: var(--radius-md);
      color: var(--text-dim);
      display: none;
    }
'''

if '.filter-toolbar {' not in index_content:
    index_content = index_content.replace('</style>', filter_css + '\n  </style>')

filter_html = '''
    <!-- Real-time Filter & Search Toolbar -->
    <div class="filter-toolbar">
      <div class="filter-search-row">
        <div class="search-input-box">
          <svg class="search-icon-svg" viewBox="0 0 24 24" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" id="brandSearchInput" placeholder="🔍 快速搜索机场、特性（如: IEPL、ChatGPT、按量、8折、暮光、微风）..." oninput="handleBrandFilter()">
        </div>
        <div class="filter-count-badge" id="filterCountBadge">
          共展示 <strong>14</strong> 个天梯评测席位
        </div>
      </div>

      <div class="filter-tags-row">
        <span style="font-size: 11px; font-weight: 700; color: var(--text-dim); margin-right: 4px;">快捷标签:</span>
        <button type="button" class="tag-filter-pill active" data-tag="all" onclick="selectQuickTag('all', this)">全部席位</button>
        <button type="button" class="tag-filter-pill" data-tag="iepl" onclick="selectQuickTag('iepl', this)">👑 IEPL 物理专线</button>
        <button type="button" class="tag-filter-pill" data-tag="fast" onclick="selectQuickTag('fast', this)">⚡ 晚高峰极速秒开</button>
        <button type="button" class="tag-filter-pill" data-tag="ai" onclick="selectQuickTag('ai', this)">🤖 ChatGPT / AI 解锁</button>
        <button type="button" class="tag-filter-pill" data-tag="cheap" onclick="selectQuickTag('cheap', this)">💰 ¥10元内平价</button>
        <button type="button" class="tag-filter-pill" data-tag="paygo" onclick="selectQuickTag('paygo', this)">📦 不限时按量计费</button>
      </div>
    </div>

    <!-- Empty State -->
    <div class="no-results-box" id="noResultsBox">
      <div style="font-size: 32px; margin-bottom: 10px;">🔍</div>
      <div style="font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 6px;">未找到匹配的机场评测</div>
      <p style="font-size: 13px; color: var(--text-dim); margin-bottom: 14px;">建议尝试其他关键词（例如：IEPL、按量、ChatGPT、微风、暮光）或重置筛选。</p>
      <button type="button" class="tag-filter-pill active" onclick="resetBrandFilter()" style="display: inline-block;">重置全部筛选 ↺</button>
    </div>
'''

if 'id="brandSearchInput"' not in index_content:
    index_content = index_content.replace(
        '    <!-- Leaderboard Cards -->\n    <div class="ranking-list">',
        filter_html + '\n    <!-- Leaderboard Cards -->\n    <div class="ranking-list" id="rankingCardsList">'
    )

filter_js = '''
    // 实时搜索与标签筛选逻辑
    let currentQuickTag = 'all';

    function selectQuickTag(tag, btn) {
      currentQuickTag = tag;
      document.querySelectorAll('.tag-filter-pill').forEach(el => el.classList.remove('active'));
      if (btn) btn.classList.add('active');
      handleBrandFilter();
    }

    function resetBrandFilter() {
      const searchInput = document.getElementById('brandSearchInput');
      if (searchInput) searchInput.value = '';
      currentQuickTag = 'all';
      document.querySelectorAll('.tag-filter-pill').forEach(el => {
        el.classList.toggle('active', el.dataset.tag === 'all');
      });
      handleBrandFilter();
    }

    function handleBrandFilter() {
      const searchInput = document.getElementById('brandSearchInput');
      const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
      const cards = document.querySelectorAll('#rankingCardsList .rank-card');
      const noResultsBox = document.getElementById('noResultsBox');
      const badge = document.getElementById('filterCountBadge');
      let visibleCount = 0;

      cards.forEach(card => {
        const text = card.innerText.toLowerCase();
        const brand = card.dataset.brand || '';
        let matchesQuery = true;
        let matchesTag = true;

        if (query) {
          matchesQuery = text.includes(query) || brand.includes(query);
        }

        if (currentQuickTag !== 'all') {
          if (currentQuickTag === 'iepl') {
            matchesTag = text.includes('iepl') || text.includes('物理专线');
          } else if (currentQuickTag === 'fast') {
            matchesTag = text.includes('0.8%') || text.includes('1.2%') || text.includes('极速') || text.includes('秒开');
          } else if (currentQuickTag === 'ai') {
            matchesTag = text.includes('chatgpt') || text.includes('gpt') || text.includes('ai');
          } else if (currentQuickTag === 'cheap') {
            matchesTag = text.includes('7.27') || text.includes('9.08') || text.includes('10.28') || text.includes('平价') || text.includes('性价比');
          } else if (currentQuickTag === 'paygo') {
            matchesTag = text.includes('按量') || text.includes('不限时');
          }
        }

        if (matchesQuery && matchesTag) {
          card.style.display = 'grid';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      if (noResultsBox) {
        noResultsBox.style.display = visibleCount === 0 ? 'block' : 'none';
      }
      if (badge) {
        badge.innerHTML = `共展示 <strong>${visibleCount}</strong> 个天梯评测席位`;
      }
    }
'''

if 'function handleBrandFilter()' not in index_content:
    index_content = index_content.replace('</script>', filter_js + '\n  </script>')

# Add JSON-LD schema for index.html
json_ld_index = '''
  <!-- SEO Structured Data Schema.org (JSON-LD) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": "https://jichangbang.top/#website",
        "url": "https://jichangbang.top/",
        "name": "机场榜",
        "alternateName": "JichangBang.top",
        "description": "2026 科学上网与机场节点量化实测天梯榜，基于晚高峰真实测速与丢包率评估",
        "potentialAction": {
          "@type": "SearchAction",
          "target": "https://jichangbang.top/?s={search_term_string}",
          "query-input": "required name=search_term_string"
        }
      },
      {
        "@type": "ItemList",
        "name": "2026 机场综合性能与性价比天梯榜",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "numberOfItems": 5,
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "隐形人机场",
            "url": "https://jichangbang.top/brand-yinxingren.html",
            "description": "全 IEPL 端到端物理专线，晚高峰 0.8% 极低丢包，ChatGPT/4K 秒开"
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": "暮光网络",
            "url": "https://jichangbang.top/brand-muguang.html",
            "description": "全 IPLC 内网专线，单节点峰值 2.5Gbps，不限设备"
          },
          {
            "@type": "ListItem",
            "position": 3,
            "name": "微风网络",
            "url": "https://jichangbang.top/brand-breezenet.html",
            "description": "Breezenet 高速大带宽保障，全流媒体 8K 支持"
          },
          {
            "@type": "ListItem",
            "position": 4,
            "name": "飞猫云",
            "url": "https://jichangbang.top/brand-feimaoyun.html",
            "description": "极速 IPLC 专线，性价比高，亚太低延迟"
          },
          {
            "@type": "ListItem",
            "position": 5,
            "name": "灵动云",
            "url": "https://jichangbang.top/brand-lingdongyun.html",
            "description": "BGP 优质专线，支持不限时按量计费保底"
          }
        ]
      }
    ]
  }
  </script>
'''

if 'type="application/ld+json"' not in index_content:
    index_content = index_content.replace('</head>', json_ld_index + '\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)
print("Updated index.html with real-time filter, toolbar and JSON-LD schema!")

# =========================================================================
# 2. Add Mobile Nav Active Pill Auto-Scroll to all 14 HTML files
# =========================================================================
auto_scroll_js = '''
    // 移动端快捷导航条自动居中当前激活项
    window.addEventListener('DOMContentLoaded', () => {
      const activePill = document.querySelector('.mobile-nav-bar .m-nav-pill.active');
      if (activePill) {
        activePill.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    });
'''

all_files = [f for f in os.listdir('.') if f.endswith('.html')]
for fname in all_files:
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'mobile-nav-bar .m-nav-pill.active' not in c:
        c = c.replace('</script>', auto_scroll_js + '\n  </script>')
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Added mobile nav auto-scroll to {fname}")

print("All optimizations applied successfully!")
