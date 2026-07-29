import { useCallback, useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

import ApplicationSidebar from "../components/layout/ApplicationSidebar";
import TopNavbar from "../components/layout/TopNavbar";
import LogoutModal from "../components/ui/LogoutModal";
import { getAssets } from "../services/assetService";
import { getCurrentUser } from "../services/userService";
import { removeToken } from "../utils/storage";
import "../pages/Dashboard/Dashboard.css";

const pageTitles = {
  "/dashboard": "Dashboard",
  "/assets": "Assets",
  "/map": "Map",
  "/settings": "Settings",
};

const getErrorMessage = (error) => {
  const detail = error.response?.data?.detail;

  if (Array.isArray(detail)) return detail.map((item) => item.msg).join(" ");
  return detail || error.message || "Please check your connection and try again.";
};

const fetchAssetList = async () => {
  const response = await getAssets();
  // Handle PaginatedResponse format { total, limit, offset, items }
  return Array.isArray(response.items) ? response.items : (Array.isArray(response) ? response : []);
};

function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [assets, setAssets] = useState([]);
  const [isLoadingAssets, setIsLoadingAssets] = useState(true);
  const [assetsError, setAssetsError] = useState("");
  const [user, setUser] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);

  const reloadAssets = useCallback(async () => {
    setIsLoadingAssets(true);
    setAssetsError("");

    try {
      setAssets(await fetchAssetList());
    } catch (error) {
      setAssetsError(getErrorMessage(error));
    } finally {
      setIsLoadingAssets(false);
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    const loadInitialData = async () => {
      const [assetsResult, userResult] = await Promise.allSettled([fetchAssetList(), getCurrentUser()]);

      if (!isMounted) return;

      if (assetsResult.status === "fulfilled") setAssets(assetsResult.value);
      else setAssetsError(getErrorMessage(assetsResult.reason));

      if (userResult.status === "fulfilled") setUser(userResult.value);
      setIsLoadingAssets(false);
    };

    loadInitialData();

    return () => {
      isMounted = false;
    };
  }, []);

  const requestLogout = () => {
    setIsSidebarOpen(false);
    setIsLogoutModalOpen(true);
  };

  const handleLogout = () => {
    removeToken();
    navigate("/", { replace: true });
  };

  return (
    <div className="app-shell">
      <ApplicationSidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        onLogout={requestLogout}
      />
      {isSidebarOpen && <button className="sidebar-backdrop" type="button" onClick={() => setIsSidebarOpen(false)} aria-label="Close navigation" />}

      <div className="app-main">
        <TopNavbar
          pageTitle={pageTitles[location.pathname] || "Dashboard"}
          user={user}
          onMenuToggle={() => setIsSidebarOpen(true)}
          onLogout={requestLogout}
        />
        <Outlet context={{ assets, isLoadingAssets, assetsError, reloadAssets, user }} />
      </div>

      <LogoutModal
        isOpen={isLogoutModalOpen}
        onCancel={() => setIsLogoutModalOpen(false)}
        onConfirm={handleLogout}
      />
    </div>
  );
}

export default AppLayout;
