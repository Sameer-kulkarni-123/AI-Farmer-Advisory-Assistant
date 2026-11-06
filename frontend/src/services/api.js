import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const api = {
  // Health
  getHealth: async () => {
    const res = await client.get('/api/health');
    return res.data;
  },

  // Languages
  getLanguages: async () => {
    const res = await client.get('/api/languages');
    return res.data;
  },

  // Sources
  getSources: async (params = {}) => {
    const res = await client.get('/api/sources', { params });
    return res.data;
  },

  getSourceById: async (id) => {
    const res = await client.get(`/api/sources/${id}`);
    return res.data;
  },

  // Chat
  sendChatMessage: async ({ message, conversationId, language, crop, region, soilType, growthStage }) => {
    const res = await client.post('/api/chat', {
      message,
      conversation_id: conversationId,
      language: language || 'en',
      crop,
      region,
      soil_type: soilType,
      growth_stage: growthStage,
    });
    return res.data;
  },

  // Advisory
  getCropAdvisory: async ({ crop, category, state, district, soilType, growthStage, language }) => {
    const res = await client.post('/api/advisory', {
      crop,
      category: category || 'cultivation',
      state: state || 'All-India',
      district,
      soil_type: soilType || 'All',
      growth_stage: growthStage || 'All',
      language: language || 'en',
    });
    return res.data;
  },

  // Conversations
  getConversations: async () => {
    const res = await client.get('/api/conversations');
    return res.data;
  },

  getConversationById: async (id) => {
    const res = await client.get(`/api/conversations/${id}`);
    return res.data;
  },

  deleteConversation: async (id) => {
    const res = await client.delete(`/api/conversations/${id}`);
    return res.data;
  },
};

