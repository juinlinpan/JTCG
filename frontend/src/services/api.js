import axios from 'axios';

// 設置基本 URL，在 Docker 環境中這應該指向後端服務名稱
// 在本地開發中，使用 localhost:8000
// 在 Docker 中，使用 /api (由 Nginx 代理到後端服務)
const API_URL = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000';

const api = {
  // 獲取所有消息
  getMessages: () => {
    return axios.get(`${API_URL}/messages/get_messages`);
  },

  // 發送新消息
  sendMessage: (message) => {
    return axios.post(`${API_URL}/messages`, message);
  },

  // 重置對話
  resetMessages: () => {
    return axios.get(`${API_URL}/messages/reset`);
  }
};

export default api;
