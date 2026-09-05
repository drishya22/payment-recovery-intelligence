function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="watermelon-mark">
          <span></span>
        </div>

        <div>
          <strong>Recovery</strong>
          <small>Intelligence</small>
        </div>
      </div>

      <div className="sidebar-section">
        <span>COMMAND</span>

        <div className="sidebar-item active">
          <i>⌁</i>
          Overview
        </div>

        <div className="sidebar-item">
          <i>!</i>
          Incidents
          <b>1</b>
        </div>

        <div className="sidebar-item">
          <i>↗</i>
          Recovery
        </div>
      </div>

      <div className="sidebar-section">
        <span>INTELLIGENCE</span>

        <div className="sidebar-item">
          <i>◌</i>
          Providers
        </div>

        <div className="sidebar-item">
          <i>◈</i>
          Decision log
        </div>
      </div>

      <div className="sidebar-bottom">
        <div className="engine-card">
          <span className="engine-dot"></span>

          <div>
            <strong>Recovery engine</strong>
            <small>Operational</small>
          </div>

          <span className="engine-arrow">↗</span>
        </div>

        <div className="sidebar-meta">
          <span>BUILDATHON EDITION</span>
          <span>V1.0</span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;