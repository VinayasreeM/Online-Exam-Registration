export const authService = {
  setToken: (token) => {
    localStorage.setItem('token', token);
  },
  
  getToken: () => {
    return localStorage.getItem('token');
  },
  
  removeToken: () => {
    localStorage.removeItem('token');
  },
  
  setUserRole: (role) => {
    localStorage.setItem('role', role);
  },
  
  getUserRole: () => {
    return localStorage.getItem('role');
  },
  
  setUserId: (userId) => {
    localStorage.setItem('userId', userId);
  },
  
  getUserId: () => {
    return localStorage.getItem('userId');
  },
  
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('userId');
  },
};
