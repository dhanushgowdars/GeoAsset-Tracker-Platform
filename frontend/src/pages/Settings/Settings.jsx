import { useOutletContext } from "react-router-dom";

const formatRole = (role) => role ? `${role.charAt(0)}${role.slice(1).toLowerCase()}` : "—";

function Settings() {
  const { user } = useOutletContext();

  return (
    <main className="dashboard-content">
      <section className="settings-page" aria-labelledby="settings-title">
        <div>
          <p className="dashboard-eyebrow">Account settings</p>
          <h2 id="settings-title">Profile</h2>
          <p>Account information associated with your current session.</p>
        </div>

        <dl className="profile-details">
          <div><dt>Username</dt><dd>{user?.username || "Loading..."}</dd></div>
          <div><dt>Email</dt><dd>{user?.email || "Loading..."}</dd></div>
          <div><dt>Role</dt><dd><span className="role-badge">{formatRole(user?.role)}</span></dd></div>
        </dl>
      </section>
    </main>
  );
}

export default Settings;
