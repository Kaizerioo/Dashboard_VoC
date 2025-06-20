import streamlit as st

html_string = """
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Voice of Customer Dashboard - Refined Aesthetics</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <script type="text/javascript">
      var gk_isXlsx = false;
      var gk_xlsxFileLookup = {};
      var gk_fileData = {};
      function filledCell(cell) {
        return cell !== "" && cell != null;
      }
      function loadFileData(filename) {
        if (gk_isXlsx && gk_xlsxFileLookup[filename]) {
          try {
            var workbook = XLSX.read(gk_fileData[filename], { type: "base64" });
            var firstSheetName = workbook.SheetNames[0];
            var worksheet = workbook.Sheets[firstSheetName];
            var jsonData = XLSX.utils.sheet_to_json(worksheet, {
              header: 1,
              blankrows: false,
              defval: "",
            });
            var filteredData = jsonData.filter((row) => row.some(filledCell));
            var headerRowIndex = filteredData.findIndex(
              (row, index) =>
                row.filter(filledCell).length >=
                filteredData[index + 1]?.filter(filledCell).length
            );
            if (headerRowIndex === -1 || headerRowIndex > 25) {
              headerRowIndex = 0;
            }
            var csv = XLSX.utils.aoa_to_sheet(
              filteredData.slice(headerRowIndex)
            );
            csv = XLSX.utils.sheet_to_csv(csv, { header: 1 });
            return csv;
          } catch (e) {
            console.error(e);
            return "";
          }
        }
        return gk_fileData[filename] || "";
      }
    </script>
    <style>
      :root {
        --font-family-apple: -apple-system, BlinkMacSystemFont, "Segoe UI",
          Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji",
          "Segoe UI Emoji", "Segoe UI Symbol";
        --card-background: #ffffff;
        --text-primary: #1d1d1f;
        --text-secondary: #4a4a4f; /* Slightly darker secondary for better contrast on new bg */
        --accent-color: #007aff;
        --accent-color-darker: #005ecb; /* For hover states on gradients */
        --border-color: #d2d2d7;
        --light-border-color: #e5e5ea;
        --shadow-color-light: rgba(0, 0, 0, 0.03);
        --shadow-color-medium: rgba(0, 0, 0, 0.06);
        --border-radius-s: 6px;
        --border-radius-m: 10px;
        --border-radius-l: 14px;
        --padding-s: 0.4rem;
        --padding-m: 0.8rem;
        --padding-l: 1.2rem;

        --font-size-base: 13.5px;
        --font-size-xs: 0.7rem;
        --font-size-s: 0.78rem;
        --font-size-m: 0.85rem;
        --font-size-label: 0.72rem;
        --font-size-l: 0.95rem;
        --font-size-xl: 1.1rem;
        --font-size-h1: 1.7rem;
        --font-size-h2: 1.3rem;
        --font-size-h3: 1.05rem;

        --soft-gradient-start: #fbfcfe;
        --soft-gradient-end: #f2f4f6;
        --chatbot-message-area-bg: #f5f5f7;
        --sidebar-bg: #fafafc; /* Slightly distinct sidebar bg */
        --header-height: 65px;
      }

      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: var(--font-family-apple);
        background: linear-gradient(
          170deg,
          var(--soft-gradient-start) 0%,
          var(--soft-gradient-end) 100%
        );
        min-height: 100vh;
        color: var(--text-primary);
        line-height: 1.5;
        overflow-x: hidden;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        font-size: var(--font-size-base);
      }

      /* Header Styles */
      .header {
        background: rgba(
          255,
          255,
          255,
          0.85
        ); /* Semi-transparent white for a modern feel */
        backdrop-filter: blur(10px); /* Frosted glass effect */
        -webkit-backdrop-filter: blur(10px);
        padding: var(--padding-m) var(--padding-l);
        border-bottom: 1px solid var(--light-border-color); /* Softer border */
        position: sticky;
        top: 0;
        z-index: 100;
      }
      .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1600px;
        margin: 0 auto;
        flex-wrap: wrap;
        gap: var(--padding-m);
      }
      .header-left {
        display: flex;
        align-items: center;
        gap: 1.2rem;
      }
      .menu-toggle {
        background: none;
        border: none;
        font-size: 1.6rem;
        cursor: pointer;
        color: var(--text-secondary);
        padding: var(--padding-s);
        border-radius: var(--border-radius-s);
        transition: background 0.2s ease, color 0.2s ease;
        z-index: 101;
      }
      .menu-toggle:hover {
        background: rgba(0, 0, 0, 0.05);
        color: var(--text-primary);
      }
      .logo {
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.01em;
      }
      .header-right {
        display: flex;
        align-items: center;
        gap: var(--padding-m);
        flex-wrap: wrap;
      }
      .header-filters {
        display: flex;
        gap: var(--padding-l);
        align-items: flex-end;
        flex-wrap: wrap;
      }

      /* Custom Checkbox Dropdown Styles */
      .custom-checkbox-dropdown-wrapper {
        position: relative;
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
      }
      .filter-label {
        font-size: var(--font-size-label);
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.04em;
        padding-left: 0.15rem;
      }
      .custom-dropdown .dropdown-trigger {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        min-width: 160px;
        padding: 0.5rem 0.8rem;
        font-size: var(--font-size-m);
        font-weight: 400;
        color: var(--text-primary);
        background-color: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-m);
        cursor: pointer;
        text-align: left;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
      }
      .custom-dropdown .dropdown-trigger:hover {
        border-color: var(--accent-color);
      }
      .custom-dropdown .dropdown-trigger:focus,
      .custom-dropdown .dropdown-trigger[aria-expanded="true"] {
        outline: none;
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2.5px
          color-mix(in srgb, var(--accent-color) 15%, transparent);
      }
      .dropdown-selected-value {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        flex-grow: 1;
      }
      .dropdown-arrow {
        width: 0.9rem;
        height: 0.9rem;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23515154' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        transition: transform 0.2s ease;
        margin-left: 0.4rem;
      }
      .custom-dropdown .dropdown-trigger[aria-expanded="true"] .dropdown-arrow {
        transform: rotate(180deg);
      }
      .custom-dropdown .dropdown-panel {
        position: absolute;
        top: calc(100% + 3px);
        left: 0;
        width: auto;
        min-width: 200px;
        max-width: 280px;
        background-color: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-m);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* Slightly more pronounced shadow for panel */
        z-index: 110;
        display: none;
        padding: 0.4rem;
        max-height: 220px;
        overflow-y: auto;
      }
      .custom-dropdown .dropdown-panel.open {
        display: block;
      }
      .checkbox-item-dd {
        display: flex;
        align-items: center;
        padding: 0.4rem 0.6rem;
        cursor: pointer;
        border-radius: var(--border-radius-s);
        transition: background-color 0.15s ease;
      }
      .checkbox-item-dd:hover {
        background-color: rgba(0, 0, 0, 0.04);
      }
      .checkbox-item-dd input[type="checkbox"] {
        margin-right: 0.6rem;
        accent-color: var(--accent-color);
        width: 14px;
        height: 14px;
        cursor: pointer;
        flex-shrink: 0;
      }
      .checkbox-item-dd label {
        font-size: var(--font-size-m);
        color: var(--text-primary);
        cursor: pointer;
        flex-grow: 1;
        line-height: 1.4;
      }

      .account-info {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        cursor: pointer;
        padding: var(--padding-s) var(--padding-m);
        border-radius: var(--border-radius-m);
        transition: background 0.2s ease;
      }
      .account-info:hover {
        background: rgba(0, 0, 0, 0.05);
      }
      .avatar {
        width: 2.25rem;
        height: 2.25rem;
        border-radius: 50%;
        background: linear-gradient(
          145deg,
          var(--accent-color) 0%,
          color-mix(in srgb, var(--accent-color) 80%, #000 10%) 100%
        );
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 500;
        font-size: 0.9rem;
      }
      .account-name {
        font-weight: 500;
        font-size: var(--font-size-m);
      }
      .account-role {
        font-size: var(--font-size-s);
        color: var(--text-secondary);
      }
      .settings-btn {
        background: none;
        border: none;
        font-size: 1.4rem;
        cursor: pointer;
        color: var(--text-secondary);
        padding: var(--padding-s);
        border-radius: var(--border-radius-s);
        transition: background 0.2s ease, color 0.2s ease;
      }
      .settings-btn:hover {
        background: rgba(0, 0, 0, 0.05);
        color: var(--text-primary);
      }

      /* Sidebar Styles */
      .sidebar {
        position: fixed;
        left: -300px;
        top: 0; /* Start from the top */
        padding-top: 0; /* Remove default padding at top */
        width: 300px;
        height: 100vh;
        background: var(--sidebar-bg);
        box-shadow: 2px 0 15px rgba(0, 0, 0, 0.04);
        transition: left 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 99;
        border-right: 1px solid var(--border-color);
        display: flex;
        flex-direction: column;
      }

      .sidebar.active {
        left: 0;
      }

      .sidebar-header {
        height: 65px; /* Match the height of your navbar */
        display: flex;
        align-items: center;
        padding: 0 var(--padding-l);
        border-bottom: 1px solid var(--light-border-color);
        background: var(--sidebar-bg);
        font-weight: 500;
        color: var(--text-primary);
        font-size: var(--font-size-l);
      }

      .sidebar-scrollable-content {
        flex-grow: 1;
        overflow-y: auto;
        padding: 1.2rem;
        padding-top: 1rem; /* Adjust top padding */
        margin-top: 0; /* Start content right below header */
      }

      .sidebar-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.35);
        opacity: 0;
        visibility: hidden;
        transition: all 0.35s ease;
        z-index: 98;
      }
      .sidebar-overlay.active {
        opacity: 1;
        visibility: visible;
      }
      .sidebar-menu {
        list-style: none;
        padding: 0;
      }
      .sidebar-menu li {
        margin-bottom: 0.2rem;
      }
      .sidebar-menu a {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.7rem var(--padding-m);
        text-decoration: none;
        color: var(--text-secondary);
        border-radius: var(--border-radius-m);
        transition: all 0.2s ease;
        font-weight: 400;
        font-size: 0.9rem;
      }
      .sidebar-menu a:hover {
        background: rgba(0, 0, 0, 0.05);
        color: var(--text-primary);
      }
      .sidebar-menu a.active {
        background: linear-gradient(
          90deg,
          var(--accent-color) 0%,
          color-mix(in srgb, var(--accent-color) 85%, #fff 5%) 100%
        );
        color: white;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2);
      }
      .sidebar-menu a.active .menu-icon {
        color: white;
      }
      .sidebar-menu .menu-icon {
        font-size: 1.1rem;
        width: 1.3rem;
        text-align: center;
        color: var(--text-secondary);
        transition: color 0.2s ease;
      }
      .sidebar-menu a:hover .menu-icon {
        color: var(--text-primary);
      }
      .sidebar-section {
        margin-top: var(--padding-l);
        padding-top: var(--padding-l);
        border-top: 1px solid var(--light-border-color);
      }
      .sidebar-section-title {
        font-size: 0.68rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: var(--padding-m);
        padding: 0 var(--padding-m);
        font-weight: 500;
      }

      /* Main Content Styles */
      .main-content {
        margin-left: 0;
        transition: margin-left 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        padding: var(--padding-l);
        width: 100%;
      }
      .dashboard-container {
        max-width: 1600px;
        margin: 0 auto;
      }
      .dashboard-header {
        text-align: left;
        margin-bottom: 2rem;
      }
      .dashboard-header h1 {
        font-size: var(--font-size-h1);
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
      }
      .dashboard-header p {
        font-size: var(--font-size-l);
        color: var(--text-secondary);
      }

      .widget-filters {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-bottom: var(--padding-l);
      }
      .widget-filter {
        padding: 0.5rem 1rem;
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-l);
        background: var(--card-background);
        font-size: var(--font-size-s);
        font-weight: 400;
        cursor: pointer;
        transition: all 0.2s ease;
        color: var(--text-secondary);
      }
      .widget-filter:hover {
        border-color: color-mix(in srgb, var(--accent-color) 60%, transparent);
        color: var(--accent-color);
      }
      .widget-filter.active {
        background: var(--accent-color);
        color: white;
        border-color: var(--accent-color);
        font-weight: 500;
      }

      .dashboard-grid {
        display: grid;
        gap: var(--padding-l);
        margin-bottom: var(--padding-l);
      }
      .widget-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: var(--padding-l);
      }
      .widget {
        background: var(--card-background);
        border-radius: var(--border-radius-l);
        padding: var(--padding-l);
        box-shadow: 0 2px 5px var(--shadow-color-light),
          0 5px 10px var(--shadow-color-medium);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        min-width: 0;
        display: flex;
        flex-direction: column;
      }
      .widget:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 8px var(--shadow-color-light),
          0 8px 18px var(--shadow-color-medium);
      }
      .widget-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: var(--padding-m);
        border-bottom: 1px solid var(--light-border-color);
        padding-bottom: var(--padding-m);
      }
      .widget-title {
        font-size: var(--font-size-h3);
        font-weight: 500;
        color: var(--text-primary);
        letter-spacing: -0.01em;
      }
      .widget-actions {
        display: flex;
        gap: 0.4rem;
      }
      .widget-action-btn {
        background: rgba(0, 0, 0, 0.04);
        border: none;
        padding: 0.5rem 0.8rem;
        border-radius: var(--border-radius-s);
        font-size: var(--font-size-s);
        font-weight: 400;
        color: var(--text-secondary);
        cursor: pointer;
        transition: all 0.2s ease;
      }
      .widget-action-btn:hover {
        background: rgba(0, 0, 0, 0.08);
        color: var(--text-primary);
      }
      .widget-action-btn.primary {
        background: linear-gradient(
          180deg,
          var(--accent-color) 0%,
          var(--accent-color-darker) 100%
        );
        color: white;
        border: none;
      }
      .widget-action-btn.primary:hover {
        background: linear-gradient(
          180deg,
          color-mix(in srgb, var(--accent-color) 95%, #fff 5%) 0%,
          var(--accent-color-darker) 100%
        );
      }

      .widget-summary {
        margin-top: auto;
        padding: var(--padding-m);
        background: rgba(0, 0, 0, 0.02); /* Subtler background */
        border-radius: var(--border-radius-m);
        font-size: var(--font-size-m);
        color: var(--text-secondary);
        border: 1px solid var(--light-border-color);
        line-height: 1.45;
      }
      .health-score {
        text-align: center;
        margin: var(--padding-m) 0;
      }
      .health-score-value {
        font-size: 3rem;
        font-weight: 500;
        color: var(--accent-color);
        margin-bottom: 0.1rem;
      }
      .health-score-value span {
        font-size: 1.8rem !important;
      }
      .health-trend {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        color: #34c759;
        font-weight: 400;
        font-size: var(--font-size-m);
      }
      .health-trend.negative {
        color: #ff3b30;
      }

      .alert-item {
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        padding: var(--padding-m);
        margin-bottom: var(--padding-m);
        border-radius: var(--border-radius-m);
        background: var(
          --card-background
        ); /* Alerts on card background for clarity */
        border-left: 4px solid;
      }
      .alert-critical {
        border-left-color: #ff3b30;
      }
      .alert-high {
        border-left-color: #ff9500;
      }
      .alert-icon {
        width: 0.6rem;
        height: 0.6rem;
        border-radius: 50%;
        flex-shrink: 0;
        margin-top: 0.3rem;
      }
      .alert-critical .alert-icon {
        background: #ff3b30;
      }
      .alert-high .alert-icon {
        background: #ff9500;
      }
      .alert-content h4 {
        font-size: var(--font-size-l);
        font-weight: 500;
        margin-bottom: 0.25rem;
        color: var(--text-primary);
      }
      .alert-metrics {
        font-size: var(--font-size-s);
        color: var(--text-secondary);
        line-height: 1.5;
      }

      .hotspot-item {
        padding: var(--padding-m);
        margin-bottom: var(--padding-m);
        border-radius: var(--border-radius-m);
        background: var(--card-background);
        border: 1px solid var(--light-border-color);
      }
      .hotspot-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.4rem;
      }
      .hotspot-header h4 {
        font-size: var(--font-size-l);
        font-weight: 500;
      }
      .impact-indicator {
        padding: 0.25rem 0.6rem;
        border-radius: var(--border-radius-l);
        font-size: var(--font-size-xs);
        font-weight: 500;
      }
      .impact-medium {
        background: color-mix(in srgb, #ff9500 18%, transparent);
        color: color-mix(in srgb, #ff9500 85%, black);
      }
      .impact-low {
        background: color-mix(in srgb, #34c759 18%, transparent);
        color: color-mix(in srgb, #34c759 85%, black);
      }

      .opportunity-item {
        padding: var(--padding-m);
        border-radius: var(--border-radius-m);
        background: var(--card-background);
        border: 1px solid var(--light-border-color);
        flex: 1;
      }
      .opportunity-item h4 {
        font-size: var(--font-size-l);
        font-weight: 500;
        margin-bottom: 0.4rem;
      }
      .opportunity-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: var(--padding-m);
      }

      .chart-container {
        position: relative;
        height: 200px;
        margin-top: var(--padding-m);
        width: 100%;
      }
      .mini-chart {
        height: 110px;
      }

      .theme-lists {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--padding-l);
      }
      .theme-list h4 {
        margin-bottom: var(--padding-m);
        color: var(--text-primary);
        font-weight: 500;
        font-size: var(--font-size-l);
      }
      .theme-item {
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.6rem;
        border-radius: var(--border-radius-m);
        font-size: var(--font-size-s);
        border: 1px solid transparent;
      }
      .positive-theme {
        background: color-mix(in srgb, #34c759 12%, transparent);
        color: color-mix(in srgb, #34c759 88%, black);
        border-color: color-mix(in srgb, #34c759 25%, transparent);
      }
      .negative-theme {
        background: color-mix(in srgb, #ff3b30 12%, transparent);
        color: color-mix(in srgb, #ff3b30 88%, black);
        border-color: color-mix(in srgb, #ff3b30 25%, transparent);
      }
      .quote-item {
        padding: 0.8rem;
        margin-top: var(--padding-m);
        border-radius: var(--border-radius-m);
        background: rgba(0, 0, 0, 0.02);
        font-size: var(--font-size-s);
        color: var(--text-secondary);
        border: 1px solid var(--light-border-color);
        font-style: italic;
        line-height: 1.4;
      }

      .btn-view-all {
        background: linear-gradient(
          180deg,
          var(--accent-color) 0%,
          var(--accent-color-darker) 100%
        );
        color: white;
        border: none;
        padding: 0.7rem var(--padding-l);
        border-radius: var(--border-radius-m);
        font-weight: 400;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
        font-size: 0.9rem;
        margin-top: var(--padding-m);
      }
      .btn-view-all:hover {
        background: linear-gradient(
          180deg,
          color-mix(in srgb, var(--accent-color) 95%, #fff 5%) 0%,
          var(--accent-color-darker) 100%
        );
        transform: translateY(-1px);
        box-shadow: 0 2px 5px rgba(0, 122, 255, 0.15);
      }
      .full-width {
        grid-column: 1 / -1;
      }

      /* Chatbot Styles */
      .chatbot-container {
        position: fixed;
        bottom: var(--padding-l);
        right: var(--padding-l);
        z-index: 1000;
      }
      .chatbot-toggle {
        background: linear-gradient(
          145deg,
          var(--accent-color) 0%,
          var(--accent-color-darker) 100%
        );
        color: white;
        border: none;
        width: 3.25rem;
        height: 3.25rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        transition: all 0.2s ease;
        font-size: 1.6rem;
      }
      .chatbot-toggle:hover {
        background: linear-gradient(
          145deg,
          color-mix(in srgb, var(--accent-color) 95%, #fff 5%) 0%,
          var(--accent-color-darker) 100%
        );
        transform: scale(1.03);
        box-shadow: 0 6px 15px rgba(0, 122, 255, 0.2);
      }
      .chatbot-window {
        display: none;
        position: absolute;
        bottom: calc(3.25rem + var(--padding-s));
        right: 0;
        width: 360px;
        height: 500px;
        background: var(--card-background);
        border-radius: var(--border-radius-l);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
        overflow: hidden;
        flex-direction: column;
        border: 1px solid var(--border-color);
      }
      .chatbot-window.active {
        display: flex;
      }
      .chatbot-header {
        background: #f8f8fa; /* Slightly cleaner than f8f8f8 */
        color: var(--text-primary);
        padding: var(--padding-m);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--light-border-color);
      }
      .chatbot-header h3 {
        font-size: 1rem;
        font-weight: 500;
      }
      .chatbot-close {
        background: none;
        border: none;
        color: var(--text-secondary);
        font-size: 1.4rem;
        cursor: pointer;
        padding: 0.2rem;
      }
      .chatbot-close:hover {
        color: var(--text-primary);
      }
      .chatbot-messages {
        flex: 1;
        padding: var(--padding-m);
        overflow-y: auto;
        background: var(--chatbot-message-area-bg);
      }
      .chatbot-message {
        margin-bottom: var(--padding-m);
        padding: 0.7rem 1rem;
        border-radius: var(--border-radius-l);
        max-width: 85%;
        font-size: var(--font-size-m);
        line-height: 1.45;
      }
      .chatbot-message.user {
        background: var(--accent-color);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: var(--border-radius-s);
      }
      .chatbot-message.bot {
        background: #e9e9ef; /* Softer bot message bg */
        color: var(--text-primary);
        border-bottom-left-radius: var(--border-radius-s);
      }
      .chatbot-message.loading {
        background: #e9e9ef;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 0.4rem;
        max-width: fit-content;
      }
      .loading-dots {
        display: inline-flex;
        gap: 4px;
      }
      .loading-dot {
        width: 8px;
        height: 8px;
        background: var(--text-secondary);
        border-radius: 50%;
        animation: bounce 0.65s infinite alternate;
      }
      .loading-dot:nth-child(2) {
        animation-delay: 0.18s;
      }
      .loading-dot:nth-child(3) {
        animation-delay: 0.36s;
      }
      @keyframes bounce {
        to {
          transform: translateY(-4px);
          opacity: 0.5;
        }
      }

      .chatbot-input {
        padding: var(--padding-m);
        border-top: 1px solid var(--light-border-color);
        display: flex;
        gap: 0.6rem;
        background: #f8f8fa;
      }
      .chatbot-input input {
        flex: 1;
        padding: 0.6rem 0.9rem;
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-l);
        font-size: var(--font-size-m);
        background: var(--card-background);
      }
      .chatbot-input input:focus {
        outline: none;
        border-color: var(--accent-color);
        box-shadow: 0 0 0 2.5px
          color-mix(in srgb, var(--accent-color) 15%, transparent);
      }
      .chatbot-input button {
        background: var(--accent-color);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: var(--border-radius-l);
        cursor: pointer;
        transition: background 0.2s ease;
        font-size: var(--font-size-m);
        font-weight: 400;
      }
      .chatbot-input button:hover {
        background: var(--accent-color-darker);
      }

      /* Responsive Styles */
      @media (max-width: 1400px) {
        .widget-row {
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
      }
      @media (max-width: 1024px) {
        .widget-row {
          grid-template-columns: 1fr;
        }
        .sidebar {
          width: 280px;
        }
        .custom-dropdown .dropdown-trigger {
          min-width: 140px;
        }
        .opportunity-grid {
          grid-template-columns: 1fr;
        }
      }
      @media (max-width: 768px) {
        :root {
          --font-size-base: 13px;
          --header-height: 130px;
        }
        .header-content {
          flex-direction: column;
          gap: var(--padding-m);
        }
        .header-left,
        .header-right {
          width: 100%;
          justify-content: space-between;
        }
        .header-filters {
          flex-direction: column;
          align-items: stretch;
          width: 100%;
          gap: var(--padding-m);
        }
        .custom-checkbox-dropdown-wrapper {
          width: 100%;
        }
        .custom-dropdown .dropdown-trigger {
          min-width: unset;
        }
        .theme-lists {
          grid-template-columns: 1fr;
        }
        .main-content {
          padding: var(--padding-m);
        }
        .dashboard-header h1 {
          font-size: 1.5rem;
        }
        .dashboard-header p {
          font-size: 0.9rem;
        }
        .widget {
          padding: var(--padding-m);
        }
        .widget-title {
          font-size: 1rem;
        }
        .chatbot-window {
          width: calc(100vw - 1.6rem);
          max-width: none;
          height: 70vh;
          right: 0.8rem;
          left: 0.8rem;
          bottom: 0.8rem;
        }
        .sidebar {
          width: 100%;
          max-width: 280px;
        }
      }
      @media (max-width: 480px) {
        :root {
          --font-size-base: 12.5px;
        }
        .header {
          padding: var(--padding-m) 0.8rem;
        }
        .logo {
          font-size: 1.4rem;
        }
        .avatar {
          width: 2rem;
          height: 2rem;
          font-size: 0.8rem;
        }
        .widget-title {
          font-size: 0.95rem;
        }
        .btn-view-all {
          padding: 0.6rem 1rem;
          font-size: 0.85rem;
        }
        .chatbot-toggle {
          width: 3rem;
          height: 3rem;
          font-size: 1.4rem;
        }
        .custom-dropdown .dropdown-trigger {
          padding: 0.5rem 0.7rem;
          font-size: 0.8rem;
        }
        .checkbox-item-dd label {
          font-size: 0.8rem;
        }
        .filter-label {
          font-size: 0.65rem;
        }
      }
    </style>
  </head>
  <body>
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-left">
          <button class="menu-toggle" onclick="toggleSidebar()">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>
          <div class="logo">VOCAL</div>
        </div>

        <div class="header-right">
          <div class="header-filters">
            <!-- Time Filter -->
            <div
              class="filter-dropdown-wrapper custom-checkbox-dropdown-wrapper"
            >
              <label class="filter-label">Time</label>
              <div class="custom-dropdown" data-filter-type="timeFilter">
                <button
                  type="button"
                  class="dropdown-trigger"
                  aria-haspopup="listbox"
                  aria-expanded="false"
                >
                  <span class="dropdown-selected-value">Select Time</span>
                  <span class="dropdown-arrow"></span>
                </button>
                <div
                  class="dropdown-panel"
                  role="listbox"
                  aria-multiselectable="false"
                >
                  <div class="checkbox-item-dd">
                    <input
                      type="radio"
                      id="time_all_dd"
                      name="timeFilter_dd_item"
                      value="all"
                    />
                    <label for="time_all_dd">All Periods</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="radio"
                      id="time_today_dd"
                      name="timeFilter_dd_item"
                      value="today"
                    />
                    <label for="time_today_dd">Today</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="radio"
                      id="time_week_dd"
                      name="timeFilter_dd_item"
                      value="week"
                    />
                    <label for="time_week_dd">This Week</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="radio"
                      id="time_month_dd"
                      name="timeFilter_dd_item"
                      value="month"
                      data-default-selected="true"
                    />
                    <label for="time_month_dd">This Month</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="radio"
                      id="time_quarter_dd"
                      name="timeFilter_dd_item"
                      value="quarter"
                    />
                    <label for="time_quarter_dd">This Quarter</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="radio"
                      id="time_year_dd"
                      name="timeFilter_dd_item"
                      value="year"
                    />
                    <label for="time_year_dd">This Year</label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Product Filter -->
            <div
              class="filter-dropdown-wrapper custom-checkbox-dropdown-wrapper"
            >
              <label class="filter-label">Product</label>
              <div class="custom-dropdown" data-filter-type="productFilter">
                <button
                  type="button"
                  class="dropdown-trigger"
                  aria-haspopup="listbox"
                  aria-expanded="false"
                >
                  <span class="dropdown-selected-value">Select Product</span>
                  <span class="dropdown-arrow"></span>
                </button>
                <div
                  class="dropdown-panel"
                  role="listbox"
                  aria-multiselectable="true"
                >
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_all_dd"
                      name="productFilter_dd_item"
                      value="all"
                      data-default-selected="true"
                    /><label for="prod_all_dd">All Products</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_mybca_dd"
                      name="productFilter_dd_item"
                      value="mobile_mybca"
                    /><label for="prod_mybca_dd">myBCA</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_bcamobile_dd"
                      name="productFilter_dd_item"
                      value="savings_bcamobile"
                    /><label for="prod_bcamobile_dd">BCA Mobile</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_kpr_dd"
                      name="productFilter_dd_item"
                      value="loans_kpr"
                    /><label for="prod_kpr_dd">KPR</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_kkb_dd"
                      name="productFilter_dd_item"
                      value="loans_kkb"
                    /><label for="prod_kkb_dd">KKB</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_ksm_dd"
                      name="productFilter_dd_item"
                      value="loans_ksm"
                    /><label for="prod_ksm_dd">KSM</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_investasi_dd"
                      name="productFilter_dd_item"
                      value="investasi"
                    /><label for="prod_investasi_dd">Investasi</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_asuransi_dd"
                      name="productFilter_dd_item"
                      value="asuransi"
                    /><label for="prod_asuransi_dd">Asuransi</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_kmk_dd"
                      name="productFilter_dd_item"
                      value="loans_kmk"
                    /><label for="prod_kmk_dd">KMK</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_kartukredit_dd"
                      name="productFilter_dd_item"
                      value="kartu_kredit"
                    /><label for="prod_kartukredit_dd">Kartu Kredit</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_edcqris_dd"
                      name="productFilter_dd_item"
                      value="edc_qris"
                    /><label for="prod_edcqris_dd">EDC & QRIS</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="prod_poketvalas_dd"
                      name="productFilter_dd_item"
                      value="poket_valas"
                    /><label for="prod_poketvalas_dd">Poket Valas</label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Channel Filter -->
            <div
              class="filter-dropdown-wrapper custom-checkbox-dropdown-wrapper"
            >
              <label class="filter-label">Channel</label>
              <div class="custom-dropdown" data-filter-type="channelFilter">
                <button
                  type="button"
                  class="dropdown-trigger"
                  aria-haspopup="listbox"
                  aria-expanded="false"
                >
                  <span class="dropdown-selected-value">Select Channel</span>
                  <span class="dropdown-arrow"></span>
                </button>
                <div
                  class="dropdown-panel"
                  role="listbox"
                  aria-multiselectable="true"
                >
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_all_dd"
                      name="channelFilter_dd_item"
                      value="all"
                      data-default-selected="true"
                    /><label for="chan_all_dd">All Channels</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_social_dd"
                      name="channelFilter_dd_item"
                      value="social_media"
                    /><label for="chan_social_dd">Social Media</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_call_dd"
                      name="channelFilter_dd_item"
                      value="call_center"
                    /><label for="chan_call_dd">Call Center</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_whatsapp_dd"
                      name="channelFilter_dd_item"
                      value="whatsapp"
                    /><label for="chan_whatsapp_dd">WhatsApp</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_webchat_dd"
                      name="channelFilter_dd_item"
                      value="webchat"
                    /><label for="chan_webchat_dd">Webchat</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_vira_dd"
                      name="channelFilter_dd_item"
                      value="vira"
                    /><label for="chan_vira_dd">VIRA</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_email_dd"
                      name="channelFilter_dd_item"
                      value="email"
                    /><label for="chan_email_dd">E-mail</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_gallup_dd"
                      name="channelFilter_dd_item"
                      value="survey_gallup"
                    /><label for="chan_gallup_dd">Survey Gallup</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_bsq_dd"
                      name="channelFilter_dd_item"
                      value="survey_bsq"
                    /><label for="chan_bsq_dd">Survey BSQ</label>
                  </div>
                  <div class="checkbox-item-dd">
                    <input
                      type="checkbox"
                      id="chan_cx_dd"
                      name="channelFilter_dd_item"
                      value="survey_cx"
                    /><label for="chan_cx_dd">Survey CX</label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="account-info" onclick="toggleAccountMenu()">
            <div class="avatar">SB</div>
            <div class="account-details">
              <div class="account-name">Sebastian</div>
              <div class="account-role">CX Manager</div>
            </div>
          </div>

          <button class="settings-btn" onclick="openSettings()">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle cx="12" cy="12" r="3"></circle>
              <path
                d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06-.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Sidebar with added header section -->
    <div class="sidebar-overlay" onclick="toggleSidebar()"></div>
    <div class="sidebar" id="sidebar">
      <div class="sidebar-header">Menu</div>
      <div class="sidebar-scrollable-content">
        <ul class="sidebar-menu">
          <li>
            <a href="#" class="active"
              ><span class="menu-icon">📊</span>Dashboard</a
            >
          </li>
          <li>
            <a href="#"><span class="menu-icon">📈</span>Analytics</a>
          </li>
          <li>
            <a href="#"><span class="menu-icon">💬</span>Feedback</a>
          </li>
          <li>
            <a href="#"><span class="menu-icon">🚨</span>Alerts</a>
          </li>
          <li>
            <a href="#"><span class="menu-icon">📋</span>Reports</a>
          </li>
        </ul>
        <div class="sidebar-section">
          <div class="sidebar-section-title">Customer Insights</div>
          <ul class="sidebar-menu">
            <li>
              <a href="#"
                ><span class="menu-icon">😊</span>Sentiment Analysis</a
              >
            </li>
            <li>
              <a href="#"><span class="menu-icon">🎯</span>Journey Mapping</a>
            </li>
            <li>
              <a href="#"
                ><span class="menu-icon">📊</span>Satisfaction Scores</a
              >
            </li>
            <li>
              <a href="#"><span class="menu-icon">🔍</span>Theme Analysis</a>
            </li>
          </ul>
        </div>
        <div class="sidebar-section">
          <div class="sidebar-section-title">Operations</div>
          <ul class="sidebar-menu">
            <li>
              <a href="#"
                ><span class="menu-icon">⚡</span>Real-time Monitoring</a
              >
            </li>
            <li>
              <a href="#"
                ><span class="menu-icon">🔮</span>Predictive Analytics</a
              >
            </li>
            <li>
              <a href="#"
                ><span class="menu-icon">📊</span>Performance Metrics</a
              >
            </li>
            <li>
              <a href="#"><span class="menu-icon">🎯</span>Action Items</a>
            </li>
          </ul>
        </div>
        <div class="sidebar-section">
          <div class="sidebar-section-title">Configuration</div>
          <ul class="sidebar-menu">
            <li>
              <a href="#"><span class="menu-icon">⚙️</span>Settings</a>
            </li>
            <li>
              <a href="#"><span class="menu-icon">👥</span>User Management</a>
            </li>
            <li>
              <a href="#"><span class="menu-icon">🔐</span>Security</a>
            </li>
            <li>
              <a href="#"><span class="menu-icon">❓</span>Help & Support</a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="dashboard-container">
        <div class="dashboard-header">
          <h1>Customer Experience Health</h1>
          <p>Real-time Insights & Performance Overview</p>
        </div>
        <div class="dashboard-grid">
          <div class="widget-row">
            <div class="widget">
              <div class="widget-header">
                <h3 class="widget-title">Customer Health Score</h3>
                <div class="widget-actions">
                  <button class="widget-action-btn">Export</button>
                </div>
              </div>
              <div class="widget-filters">
                <span class="widget-filter active">Real-time</span>
                <span class="widget-filter">Daily Trend</span>
                <span class="widget-filter">Comparison</span>
              </div>
              <div class="health-score">
                <div class="health-score-value">
                  82<span
                    style="font-size: 1.8rem; color: var(--text-secondary)"
                    >%</span
                  >
                </div>
                <div class="health-trend">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.8"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <line x1="12" y1="19" x2="12" y2="5"></line>
                    <polyline points="5 12 12 5 19 12"></polyline>
                  </svg>
                  <span>1.5% vs. last month</span>
                </div>
              </div>
              <div class="chart-container mini-chart">
                <canvas id="healthTrendChart"></canvas>
              </div>
              <div class="widget-summary">
                Overall customer satisfaction is strong, showing a positive
                trend this month.
              </div>
            </div>
            <div class="widget">
              <div class="widget-header">
                <h3 class="widget-title">Critical Alerts</h3>
                <div class="widget-actions">
                  <button class="widget-action-btn primary">
                    Acknowledge All
                  </button>
                </div>
              </div>
              <div class="widget-filters">
                <span class="widget-filter active">Critical</span>
                <span class="widget-filter">High</span>
                <span class="widget-filter">Medium</span>
                <span class="widget-filter">All</span>
              </div>
              <div class="alert-item alert-critical">
                <div class="alert-icon"></div>
                <div class="alert-content">
                  <h4>Sudden Spike in Negative Sentiment</h4>
                  <div class="alert-metrics">
                    Mobile App Update X.Y: 45% negative<br />
                    Volume: 150 mentions / 3 hrs<br />
                    Issues: Login Failed, App Crashing
                  </div>
                </div>
              </div>
              <div class="alert-item alert-high">
                <div class="alert-icon"></div>
                <div class="alert-content">
                  <h4>High Churn Risk Pattern Detected</h4>
                  <div class="alert-metrics">
                    Pattern: Repeated Billing Errors - Savings<br />
                    12 unique customer patterns<br />
                    Avg. sentiment: -0.8
                  </div>
                </div>
              </div>
              <button class="btn-view-all">View All Alerts</button>
            </div>
            <div class="widget">
              <div class="widget-header">
                <h3 class="widget-title">Predictive Hotspots</h3>
                <div class="widget-actions">
                  <button class="widget-action-btn primary">
                    Create Action
                  </button>
                </div>
              </div>
              <div class="widget-filters">
                <span class="widget-filter active">Emerging</span>
                <span class="widget-filter">Trending</span>
                <span class="widget-filter">Predicted</span>
              </div>
              <div class="hotspot-item">
                <div class="hotspot-header">
                  <h4>New Overdraft Policy Confusion</h4>
                  <span class="impact-indicator impact-medium"
                    >Medium Impact</span
                  >
                </div>
                <div class="alert-metrics">
                  'Confused' Language: +30% WoW<br />
                  Keywords: "don't understand", "how it works"
                </div>
              </div>
              <div class="hotspot-item">
                <div class="hotspot-header">
                  <h4>Intl. Transfer UI Issues</h4>
                  <span class="impact-indicator impact-low">Low Impact</span>
                </div>
                <div class="alert-metrics">
                  Task Abandonment: +15% MoM<br />
                  Negative sentiment: 'Beneficiary Setup'
                </div>
              </div>
              <div class="widget-summary">
                Monitor emerging confusion on overdrafts and usability for
                international transfers.
              </div>
            </div>
          </div>
          <div class="widget full-width">
            <div class="widget-header">
              <h3 class="widget-title">Customer Voice Snapshot</h3>
              <div class="widget-actions">
                <button class="widget-action-btn">Drill Down</button>
                <button class="widget-action-btn">Export</button>
              </div>
            </div>
            <div class="widget-filters">
              <span class="widget-filter active">Overview</span>
              <span class="widget-filter">Sentiment</span>
              <span class="widget-filter">Intent</span>
              <span class="widget-filter">Volume</span>
            </div>
            <div
              style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: var(--padding-l);
                padding-top: var(--padding-m);
              "
            >
              <div>
                <h4
                  style="
                    margin-bottom: 0.8rem;
                    font-weight: 400;
                    font-size: var(--font-size-l);
                    color: var(--text-secondary);
                  "
                >
                  Sentiment Distribution
                </h4>
                <div class="chart-container" style="height: 230px">
                  <canvas id="sentimentChart"></canvas>
                </div>
              </div>
              <div>
                <h4
                  style="
                    margin-bottom: 0.8rem;
                    font-weight: 400;
                    font-size: var(--font-size-l);
                    color: var(--text-secondary);
                  "
                >
                  Intent Distribution
                </h4>
                <div class="chart-container" style="height: 230px">
                  <canvas id="intentChart"></canvas>
                </div>
              </div>
              <div>
                <h4
                  style="
                    margin-bottom: 0.8rem;
                    font-weight: 400;
                    font-size: var(--font-size-l);
                    color: var(--text-secondary);
                  "
                >
                  Volume Trend (30 Days)
                </h4>
                <div class="chart-container" style="height: 230px">
                  <canvas id="volumeChart"></canvas>
                </div>
              </div>
            </div>
            <div class="widget-summary">
              Positive sentiment leads at 65%. Information-seeking is top intent
              (40%). Volume shows steady increase.
            </div>
          </div>
          <div class="widget full-width">
            <div class="widget-header">
              <h3 class="widget-title">Top Customer Themes</h3>
              <div class="widget-actions">
                <button class="widget-action-btn primary">
                  Analyze Themes
                </button>
              </div>
            </div>
            <div class="widget-filters">
              <span class="widget-filter active">Top 10</span>
              <span class="widget-filter">Trending</span>
              <span class="widget-filter">Emerging</span>
              <span class="widget-filter">Declining</span>
            </div>
            <div class="theme-lists">
              <div>
                <h4 style="color: #34c759; padding-bottom: 0.5rem">
                  Top Positive Themes
                </h4>
                <div class="theme-item positive-theme">
                  Fast Customer Service
                </div>
                <div class="theme-item positive-theme">Easy Mobile Banking</div>
                <div class="theme-item positive-theme">Helpful Staff</div>
                <div class="quote-item">
                  "Support resolved my issue in minutes! So efficient."
                </div>
              </div>
              <div>
                <h4 style="color: #ff3b30; padding-bottom: 0.5rem">
                  Top Negative Themes
                </h4>
                <div class="theme-item negative-theme">
                  App Technical Issues
                </div>
                <div class="theme-item negative-theme">
                  Long Wait Times (Call)
                </div>
                <div class="theme-item negative-theme">Fee Transparency</div>
                <div class="quote-item">
                  "The app keeps crashing after the latest update. Very
                  frustrating."
                </div>
              </div>
            </div>
          </div>
          <div class="widget full-width">
            <div class="widget-header">
              <h3 class="widget-title">Opportunity Radar</h3>
              <div class="widget-actions">
                <button class="widget-action-btn primary">Prioritize</button>
              </div>
            </div>
            <div class="widget-filters">
              <span class="widget-filter active">High Value</span>
              <span class="widget-filter">Quick Wins</span>
              <span class="widget-filter">Strategic</span>
            </div>
            <div class="opportunity-grid">
              <div class="opportunity-item">
                <h4>🎉 Delightful: Instant Card Activation</h4>
                <div class="alert-metrics">
                  75 delight mentions this week (Sentiment: +0.95)<br />
                  Keywords: "amazing", "so easy", "instant"<br />
                  <strong>Action:</strong> Amplify in marketing? Benchmark?
                </div>
              </div>
              <div class="opportunity-item">
                <h4>💰 Cross-Sell: Mortgage Inquiries +15%</h4>
                <div class="alert-metrics">
                  Mortgage info seeking: +15% WoW<br />
                  Related: Savings, Financial Planning<br />
                  <strong>Action:</strong> Target with relevant mortgage info?
                </div>
              </div>
              <div class="opportunity-item">
                <h4>⭐ Service Excellence: Complex Issues</h4>
                <div class="alert-metrics">
                  25 positive mentions for complex issue resolution<br />
                  Agents: A, B, C praised.<br />
                  <strong>Action:</strong> Identify best practices? Recognize
                  agents?
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chatbot -->
    <div class="chatbot-container">
      <button class="chatbot-toggle" onclick="toggleChatbot()">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path
            d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
          ></path>
        </svg>
      </button>
      <div class="chatbot-window" id="chatbotWindow">
        <div class="chatbot-header">
          <h3>VIRA</h3>
          <button class="chatbot-close" onclick="toggleChatbot()">✕</button>
        </div>
        <div class="chatbot-messages" id="chatbotMessages">
          <div class="chatbot-message bot">
            Hello! I'm <b>VIRA</b> your AI assistant. How can I help with the
            dashboard today?
          </div>
        </div>
        <div class="chatbot-input">
          <input
            type="text"
            id="chatbotInput"
            placeholder="Ask about insights, alerts..."
          />
          <button onclick="sendChatbotMessage()">Send</button>
        </div>
      </div>
    </div>

    <script>
      const healthScoreData = {
        today: {
          labels: ["9 AM", "11 AM", "1 PM", "3 PM", "5 PM", "7 PM", "9 PM"],
          values: [78, 76, 80, 79, 81, 83, 84],
          score: 84,
          trend: "+2.5%",
          trendPositive: true,
          trendLabel: "vs. yesterday",
        },
        week: {
          labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          values: [79, 78, 80, 81, 83, 84, 85],
          score: 85,
          trend: "+1.8%",
          trendPositive: true,
          trendLabel: "vs. last week",
        },
        month: {
          labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
          values: [79, 80, 81, 82],
          score: 82,
          trend: "+1.5%",
          trendPositive: true,
          trendLabel: "vs. last month",
        },
        quarter: {
          labels: ["Jan", "Feb", "Mar"],
          values: [76, 79, 83],
          score: 83,
          trend: "+3.2%",
          trendPositive: true,
          trendLabel: "vs. last quarter",
        },
        year: {
          labels: ["Q1", "Q2", "Q3", "Q4"],
          values: [75, 77, 80, 84],
          score: 84,
          trend: "+4.1%",
          trendPositive: true,
          trendLabel: "vs. last year",
        },
        all: {
          labels: ["2019", "2020", "2021", "2022", "2023", "2024"],
          values: [73, 71, 75, 78, 80, 83],
          score: 83,
          trend: "+10.4%",
          trendPositive: true,
          trendLabel: "over 5 years",
        },
      };

      function toggleSidebar() {
        const sidebar = document.getElementById("sidebar");
        const header = document.querySelector(".header");
        const overlay = document.querySelector(".sidebar-overlay");

        // Get the current header height
        const headerHeight = header.offsetHeight;

        // Set the sidebar top position to match header height
        if (!sidebar.classList.contains("active")) {
          // Only set these when opening
          sidebar.style.top = `${headerHeight}px`;
          sidebar.style.height = `calc(100vh - ${headerHeight}px)`;
        }

        sidebar.classList.toggle("active");
        overlay.classList.toggle("active");
      }
      function toggleAccountMenu() {
        console.log("Account menu clicked");
      }
      function openSettings() {
        console.log("Settings clicked");
      }
      function toggleChatbot() {
        const cw = document.getElementById("chatbotWindow");
        cw.classList.toggle("active");
        if (cw.classList.contains("active"))
          document.getElementById("chatbotInput").focus();
      }
      async function sendChatbotMessage() {
        const input = document.getElementById("chatbotInput"),
          msgs = document.getElementById("chatbotMessages"),
          txt = input.value.trim();
        if (!txt) return;
        const userMsg = document.createElement("div");
        userMsg.className = "chatbot-message user";
        userMsg.textContent = txt;
        msgs.appendChild(userMsg);
        const loadMsg = document.createElement("div");
        loadMsg.className = "chatbot-message loading";
        loadMsg.innerHTML = `<span>Thinking</span><span class="loading-dots"><span class="loading-dot"></span><span class="loading-dot"></span><span class="loading-dot"></span></span>`;
        msgs.appendChild(loadMsg);
        msgs.scrollTop = msgs.scrollHeight;
        input.value = "";
        await new Promise((r) => setTimeout(r, 700 + Math.random() * 300));
        loadMsg.remove();
        const botMsg = document.createElement("div");
        botMsg.className = "chatbot-message bot";
        botMsg.textContent = getBotResponse(txt);
        msgs.appendChild(botMsg);
        msgs.scrollTop = msgs.scrollHeight;
      }
      function getBotResponse(msg) {
        const lm = msg.toLowerCase();
        if (lm.includes("health score"))
          return "Customer Health Score is 82%, up 1.5% from last month. More details?";
        if (lm.includes("alerts"))
          return "2 critical alerts: Mobile app sentiment spike & Churn risk from billing errors. Details or actions?";
        if (lm.includes("hotspots"))
          return "Hotspots: Overdraft policy confusion (medium impact) & Intl. transfer UI issues (low impact). Explore further?";
        if (lm.includes("opportunities"))
          return "Opportunities: Promote instant card activation, target mortgage inquiries, scale service excellence. Interested in one?";
        if (lm.includes("thank")) return "You're welcome! Anything else?";
        return 'I can help with dashboard insights. Try "health score trends", "summarize alerts", or "top opportunities".';
      }

      let healthTrendChartInstance,
        sentimentChartInstance,
        intentChartInstance,
        volumeChartInstance;
      function updateHealthScoreWidget(timePeriod) {
        // Get the data for the selected time period
        const data = healthScoreData[timePeriod];
        if (!data) return;

        // Update the health score value
        const healthScoreValueElement = document.querySelector(
          ".health-score-value"
        );
        if (healthScoreValueElement) {
          healthScoreValueElement.innerHTML = `${data.score}<span style="font-size: 1.8rem; color: var(--text-secondary)">%</span>`;
        }

        // Update the trend
        const healthTrendElement = document.querySelector(".health-trend");
        if (healthTrendElement) {
          healthTrendElement.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="${data.trendPositive ? "19" : "5"}" x2="12" y2="${
            data.trendPositive ? "5" : "19"
          }"></line>
        <polyline points="${
          data.trendPositive ? "5 12 12 5 19 12" : "5 12 12 19 19 12"
        }"></polyline>
      </svg>
      <span>${data.trend} ${data.trendLabel}</span>
    `;

          if (data.trendPositive) {
            healthTrendElement.classList.remove("negative");
          } else {
            healthTrendElement.classList.add("negative");
          }
        }

        // Update the chart if it exists
        if (healthTrendChartInstance) {
          healthTrendChartInstance.data.labels = data.labels;
          healthTrendChartInstance.data.datasets[0].data = data.values;
          healthTrendChartInstance.options.scales.y.min =
            Math.min(...data.values) - 2;
          healthTrendChartInstance.options.scales.y.max =
            Math.max(...data.values) + 2;
          healthTrendChartInstance.update();
        }
      }
      document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".widget-filter").forEach((f) =>
          f.addEventListener("click", function () {
            this.closest(".widget, .full-width")
              ?.querySelectorAll(".widget-filter")
              .forEach((i) => i.classList.remove("active"));
            this.classList.add("active");
          })
        );

        document.querySelectorAll(".custom-dropdown").forEach((dropdown) => {
          const trigger = dropdown.querySelector(".dropdown-trigger"),
            panel = dropdown.querySelector(".dropdown-panel"),
            display = trigger.querySelector(".dropdown-selected-value"),
            cbs = panel.querySelectorAll('input[type="checkbox"]'),
            type = dropdown.dataset.filterType;
          function updateDisp() {
            const chkd = Array.from(cbs).filter(
                (cb) => cb.checked && cb.value !== "all"
              ),
              allCb = panel.querySelector(
                'input[type="checkbox"][value="all"]'
              );
            if (allCb && allCb.checked)
              display.textContent =
                allCb.parentElement.querySelector("label").textContent;
            else if (chkd.length === 0)
              display.textContent = `Select ${type.replace("Filter", "")}...`;
            else if (chkd.length === 1)
              display.textContent =
                chkd[0].parentElement.querySelector("label").textContent;
            else display.textContent = `${chkd.length} selected`;
          }
          function setDefault() {
            let specDef = false;
            cbs.forEach((cb) => {
              cb.checked = cb.dataset.defaultSelected === "true";
              if (cb.checked) specDef = true;
            });
            const allCb = panel.querySelector(
              'input[type="checkbox"][value="all"]'
            );
            if (allCb) {
              if (!specDef) allCb.checked = true;
              if (allCb.checked)
                cbs.forEach((cb) => {
                  if (cb.value !== "all") {
                    cb.checked = false;
                    cb.disabled = true;
                  }
                });
            }
            updateDisp();
          }
          setDefault();
          trigger.addEventListener("click", (e) => {
            e.stopPropagation();
            const isOpen = panel.classList.toggle("open");
            trigger.setAttribute("aria-expanded", isOpen.toString());
            document
              .querySelectorAll(".custom-dropdown .dropdown-panel.open")
              .forEach((op) => {
                if (op !== panel) {
                  op.classList.remove("open");
                  op.previousElementSibling.setAttribute(
                    "aria-expanded",
                    "false"
                  );
                }
              });
          });
          cbs.forEach((cbx) =>
            cbx.addEventListener("change", () => {
              const allCb = panel.querySelector(
                'input[type="checkbox"][value="all"]'
              );
              if (allCb) {
                if (cbx.value === "all")
                  cbs.forEach((cb) => {
                    if (cb.value !== "all") {
                      cb.checked = false;
                      cb.disabled = cbx.checked;
                    }
                  });
                else {
                  const specChkd =
                    Array.from(cbs).filter(
                      (cb) => cb.checked && cb.value !== "all"
                    ).length > 0;
                  allCb.checked = !specChkd;
                  if (allCb.checked)
                    cbs.forEach((cb) => {
                      if (cb.value !== "all") cb.disabled = true;
                    });
                  else
                    cbs.forEach((cb) => {
                      if (cb.value !== "all") cb.disabled = false;
                    });
                }
              }
              updateDisp();
              collectAndApplyGlobalFilters();
            })
          );
        });
        document.addEventListener("click", (e) => {
          document
            .querySelectorAll(".custom-dropdown .dropdown-panel.open")
            .forEach((p) => {
              if (!p.parentElement.contains(e.target)) {
                p.classList.remove("open");
                p.previousElementSibling.setAttribute("aria-expanded", "false");
              }
            });
        });
        document
          .getElementById("chatbotInput")
          ?.addEventListener(
            "keypress",
            (e) => e.key === "Enter" && sendChatbotMessage()
          );
        collectAndApplyGlobalFilters();
      });

      function collectAndApplyGlobalFilters() {
        const filters = {};

        // Handle checkbox-based filters (products and channels) and radio-based filter (time)
        document.querySelectorAll(".custom-dropdown").forEach((dd) => {
          const type = dd.dataset.filterType;
          filters[type] = [];

          if (type === "timeFilter") {
            // For time filter, find the selected radio button
            const selectedRadio = dd.querySelector(
              'input[type="radio"]:checked'
            );
            if (selectedRadio) {
              filters[type] = [selectedRadio.value];
            } else {
              filters[type] = ["month"]; // Default
            }
          } else {
            // For checkbox filters
            dd.querySelectorAll(
              '.dropdown-panel input[type="checkbox"]:checked'
            ).forEach((cb) => {
              filters[type].push(cb.value);
            });
            if (filters[type].length === 0) filters[type].push("all"); // Default to all if nothing selected
          }
        });

        console.log("Applied filters:", filters);
        updateDashboardData(filters);

        // Also update the health score widget directly
        if (filters.timeFilter && filters.timeFilter.length > 0) {
          updateHealthScoreWidget(filters.timeFilter[0]);
        }
      }
      function updateDashboardData(filters) {
        console.log("Updating with filters:", filters);
        [
          healthTrendChartInstance,
          sentimentChartInstance,
          intentChartInstance,
          volumeChartInstance,
        ].forEach((c) => c?.destroy());
        initializeCharts(filters);
      }

      Chart.defaults.font.family = getComputedStyle(document.documentElement)
        .getPropertyValue("--font-family-apple")
        .trim();
      Chart.defaults.font.size = 10.5;
      Chart.defaults.color = getComputedStyle(document.documentElement)
        .getPropertyValue("--text-secondary")
        .trim();
      Chart.defaults.borderColor = getComputedStyle(document.documentElement)
        .getPropertyValue("--light-border-color")
        .trim();

      function initializeCharts(filters = {}) {
        console.log("Init charts, filters:", filters);

        // Get current time period from filters
        let currentTimePeriod = "month"; // default
        if (
          filters.timeFilter &&
          filters.timeFilter.length > 0 &&
          filters.timeFilter[0] !== "all"
        ) {
          currentTimePeriod = filters.timeFilter[0];
        }

        // Other multipliers as before
        let pM =
          filters.productFilter?.includes("all") ||
          !filters.productFilter ||
          filters.productFilter.length === 0
            ? 1
            : 0.8;
        let cF =
          filters.channelFilter?.includes("all") ||
          !filters.channelFilter ||
          filters.channelFilter.length === 0
            ? 1
            : filters.channelFilter.includes("social_media")
            ? 0.6
            : 0.9;

        // Get health score data for current time period
        const healthData =
          healthScoreData[currentTimePeriod] || healthScoreData.month;

        const healthCtx = document
          .getElementById("healthTrendChart")
          .getContext("2d");
        const healthFillGrad = healthCtx.createLinearGradient(
          0,
          0,
          0,
          healthCtx.canvas.height * 0.8
        );
        healthFillGrad.addColorStop(0, "rgba(52,199,89,0.18)");
        healthFillGrad.addColorStop(1, "rgba(52,199,89,0.01)");

        healthTrendChartInstance = new Chart(healthCtx, {
          type: "line",
          data: {
            labels: healthData.labels,
            datasets: [
              {
                data: healthData.values,
                borderColor: "#34c759",
                backgroundColor: healthFillGrad,
                fill: true,
                tension: 0.35,
                pointRadius: 0,
                pointHoverRadius: 4,
                borderWidth: 2,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                mode: "index",
                intersect: false,
                bodyFont: { size: 10 },
                titleFont: { size: 11 },
              },
            },
            scales: {
              x: { grid: { display: false }, ticks: { font: { size: 9 } } },
              y: {
                grid: { drawBorder: false },
                ticks: {
                  font: { size: 9 },
                  precision: 0,
                  stepSize: 5,
                  min: Math.min(...healthData.values) - 2,
                  max: Math.max(...healthData.values) + 2,
                },
              },
            },
            animation: { duration: 400 },
          },
        });

        const sentimentCtx = document
          .getElementById("sentimentChart")
          .getContext("2d");
        sentimentChartInstance = new Chart(sentimentCtx, {
          type: "doughnut",
          data: {
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [
              {
                data: [
                  (60 + Math.random() * 10) * pM,
                  (20 + Math.random() * 5) * pM,
                  (10 + Math.random() * 5) * pM,
                ],
                backgroundColor: ["#34c759", "#a2a2a7", "#ff3b30"],
                borderWidth: 0,
                hoverOffset: 6,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "75%",
            plugins: {
              legend: {
                position: "bottom",
                labels: {
                  usePointStyle: true,
                  pointStyle: "circle",
                  padding: 15,
                  font: { size: 10 },
                },
              },
              tooltip: {
                callbacks: {
                  label: (ctx) => `${ctx.label}: ${ctx.formattedValue}%`,
                },
              },
            },
            animation: { duration: 400 },
          },
        });

        const intentCtx = document
          .getElementById("intentChart")
          .getContext("2d");
        intentChartInstance = new Chart(intentCtx, {
          type: "bar",
          data: {
            labels: [
              "Info Seeking",
              "Complaint",
              "Service Request",
              "Feedback",
            ],
            datasets: [
              {
                data: [
                  35 + Math.random() * 10,
                  20 + Math.random() * 5,
                  20 + Math.random() * 5,
                  10 + Math.random() * 5,
                ],
                backgroundColor: ["#007aff", "#ff9500", "#5856d6", "#ffcc00"],
                borderRadius: 4,
                barPercentage: 0.6,
                categoryPercentage: 0.7,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: "y",
            plugins: { legend: { display: false } },
            scales: {
              x: { grid: { drawBorder: false }, ticks: { font: { size: 10 } } },
              y: { grid: { display: false }, ticks: { font: { size: 10 } } },
            },
            animation: { duration: 400 },
          },
        });

        const volumeCtx = document
          .getElementById("volumeChart")
          .getContext("2d");
        const volFillGrad = volumeCtx.createLinearGradient(
          0,
          0,
          0,
          volumeCtx.canvas.height * 0.8
        );
        volFillGrad.addColorStop(0, "rgba(0,122,255,0.18)");
        volFillGrad.addColorStop(1, "rgba(0,122,255,0.01)");
        const volData = Array.from(
          { length: 30 },
          (_, i) => (400 + Math.random() * 300 + i * 5) * cF
        );
        volumeChartInstance = new Chart(volumeCtx, {
          type: "line",
          data: {
            labels: Array.from({ length: 30 }, (_, i) => `${i + 1}`),
            datasets: [
              {
                data: volData,
                borderColor: "#007aff",
                backgroundColor: volFillGrad,
                fill: true,
                tension: 0.35,
                pointRadius: 0,
                pointHoverRadius: 4,
                borderWidth: 2,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: {
                grid: { display: false },
                ticks: { font: { size: 9 }, autoSkip: true, maxTicksLimit: 8 },
              },
              y: {
                grid: { drawBorder: false },
                ticks: {
                  font: { size: 9 },
                  precision: 0,
                  min: Math.min(...volData) - 20,
                  max: Math.max(...volData) + 20,
                },
              },
            },
            animation: { duration: 400 },
          },
        });
      }
      window.addEventListener("resize", () => {
        if (window.innerWidth > 1024)
          document.querySelector(".sidebar-overlay").classList.remove("active");
      });
      document.addEventListener("DOMContentLoaded", function () {
        // Get all radio buttons in the time filter dropdown
        const timeRadioButtons = document.querySelectorAll(
          'input[name="timeFilter_dd_item"]'
        );

        // Set the default selection
        timeRadioButtons.forEach((radio) => {
          if (radio.dataset.defaultSelected === "true") {
            radio.checked = true;
            // Update the dropdown display text
            const selectedLabel = radio.nextElementSibling.textContent;
            const timeDropdownDisplay = document.querySelector(
              '[data-filter-type="timeFilter"] .dropdown-selected-value'
            );
            if (timeDropdownDisplay) {
              timeDropdownDisplay.textContent = selectedLabel;
            }
          }
        });

        // Add event listeners to all radio buttons
        timeRadioButtons.forEach((radio) => {
          radio.addEventListener("change", function () {
            if (this.checked) {
              // Get the label text
              const selectedLabel = this.nextElementSibling.textContent;

              // Update the dropdown display text
              const timeDropdownDisplay = document.querySelector(
                '[data-filter-type="timeFilter"] .dropdown-selected-value'
              );
              if (timeDropdownDisplay) {
                timeDropdownDisplay.textContent = selectedLabel;
              }

              // Close the dropdown after selection
              const panel = this.closest(".dropdown-panel");
              panel.classList.remove("open");
              panel.previousElementSibling.setAttribute(
                "aria-expanded",
                "false"
              );

              // Apply filters
              collectAndApplyGlobalFilters();
            }
          });
        });
      });
    </script>
  </body>
</html>

"""

st.html(html_string, height=300, scrolling=True) # scrolling=True jika kontennya panjang

