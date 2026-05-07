class RBAC {
  static bool canManageUsers(String role) {
    return role == "admin";
  }

  static bool canViewDashboard(String role) {
    return role == "admin";
  }

  static bool canManageStock(String role) {
    return role == "admin" || role == "pharmacy";
  }

  static bool canViewOrders(String role) {
    return role != "customer";
  }

  static bool isAdmin(String role) {
    return role == "admin";
  }
}
