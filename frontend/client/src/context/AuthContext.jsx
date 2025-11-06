import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Configure axios defaults
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
  
  useEffect(() => {
    // Check if user is logged in on mount
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (token && userData) {
      setUser(JSON.parse(userData))
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      // FastAPI expects form data for OAuth2
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)
      
      const response = await axios.post(`${API_URL}/api/auth/login`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      const { access_token, user: userData } = response.data
      
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(userData))
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      
      setUser(userData)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed'
      }
    }
  }

  const register = async (email, password, fullName, phone = null) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/register`, {
        email,
        password,
        full_name: fullName,
        phone
      })
      
      return { 
        success: true, 
        data: response.data 
      }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed'
      }
    }
  }

  const verifyEmailOTP = async (email, otp) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/verify-email-otp`, {
        email,
        otp
      })
      
      return { 
        success: true, 
        message: response.data.message 
      }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Verification failed'
      }
    }
  }

  const resendEmailOTP = async (email) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/resend-email-otp`, {
        email
      })
      
      return { 
        success: true, 
        data: response.data 
      }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Failed to resend OTP'
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
  }

  const value = {
    user,
    loading,
    login,
    register,
    verifyEmailOTP,
    resendEmailOTP,
    logout
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
