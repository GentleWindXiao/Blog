import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const fetchBlogs = () => axios.get(`${API_BASE}/blogs/`);
export const fetchBlogDetail = (slug) => axios.get(`${API_BASE}/blogs/${slug}/`);
export const likeBlog = (slug) => axios.post(`${API_BASE}/blogs/${slug}/like/`);
export const viewBlog = (slug) => axios.post(`${API_BASE}/blogs/${slug}/view/`);
