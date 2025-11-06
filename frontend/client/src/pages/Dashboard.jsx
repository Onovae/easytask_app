import { useState, useEffect } from 'react'
import axios from 'axios'

const PRIORITIES = ['low', 'medium', 'high']
const LABELS = ['work', 'personal', 'urgent', 'other']

const PRIORITY_COLORS = {
  high: 'bg-red-100 text-red-800 border-red-300',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  low: 'bg-green-100 text-green-800 border-green-300'
}

const LABEL_COLORS = {
  work: 'bg-blue-100 text-blue-800',
  personal: 'bg-purple-100 text-purple-800',
  urgent: 'bg-red-100 text-red-800',
  other: 'bg-gray-100 text-gray-800'
}

export default function Dashboard() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showNewTask, setShowNewTask] = useState(false)
  const [filterLabel, setFilterLabel] = useState('')
  const [filterPriority, setFilterPriority] = useState('')
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    reminder_time: '',
    priority: 'medium',
    label: 'other'
  })

  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

  useEffect(() => {
    fetchTasks()
  }, [filterLabel, filterPriority])

  const fetchTasks = async () => {
    try {
      let url = `${API_URL}/api/tasks`
      const params = new URLSearchParams()
      
      if (filterLabel) params.append('label', filterLabel)
      if (filterPriority) params.append('priority', filterPriority)
      
      if (params.toString()) {
        url += `?${params.toString()}`
      }
      
      const response = await axios.get(url)
      setTasks(response.data)
      setError('')
    } catch (err) {
      setError('Failed to load tasks')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (e) => {
    e.preventDefault()
    
    try {
      const taskData = {
        title: newTask.title,
        description: newTask.description,
        priority: newTask.priority,
        label: newTask.label,
        ...(newTask.reminder_time && { reminder_time: newTask.reminder_time })
      }

      await axios.post(`${API_URL}/api/tasks`, taskData)
      
      setNewTask({ title: '', description: '', reminder_time: '', priority: 'medium', label: 'other' })
      setShowNewTask(false)
      fetchTasks()
    } catch (err) {
      setError('Failed to create task')
      console.error(err)
    }
  }

  const handleToggleTask = async (taskId, currentStatus) => {
    try {
      await axios.patch(`${API_URL}/api/tasks/${taskId}`, {
        is_done: !currentStatus
      })
      fetchTasks()
    } catch (err) {
      setError('Failed to update task')
      console.error(err)
    }
  }

  const handleDeleteTask = async (taskId) => {
    if (!confirm('Are you sure you want to delete this task?')) return
    
    try {
      await axios.delete(`${API_URL}/api/tasks/${taskId}`)
      fetchTasks()
    } catch (err) {
      setError('Failed to delete task')
      console.error(err)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading tasks...</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <button
          onClick={() => setShowNewTask(!showNewTask)}
          className="btn-primary"
        >
          {showNewTask ? 'Cancel' : '+ New Task'}
        </button>
      </div>

      {/* Filters */}
      <div className="mb-6 flex flex-wrap gap-3">
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Filter by Label</label>
          <select
            value={filterLabel}
            onChange={(e) => setFilterLabel(e.target.value)}
            className="input-field py-2 text-sm"
          >
            <option value="">All Labels</option>
            {LABELS.map(label => (
              <option key={label} value={label}>{label.charAt(0).toUpperCase() + label.slice(1)}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Filter by Priority</label>
          <select
            value={filterPriority}
            onChange={(e) => setFilterPriority(e.target.value)}
            className="input-field py-2 text-sm"
          >
            <option value="">All Priorities</option>
            {PRIORITIES.map(priority => (
              <option key={priority} value={priority}>{priority.charAt(0).toUpperCase() + priority.slice(1)}</option>
            ))}
          </select>
        </div>

        {(filterLabel || filterPriority) && (
          <div className="flex items-end">
            <button
              onClick={() => {
                setFilterLabel('')
                setFilterPriority('')
              }}
              className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900"
            >
              Clear Filters
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {showNewTask && (
        <div className="card mb-6">
          <h3 className="text-lg font-semibold mb-4">Create New Task</h3>
          <form onSubmit={handleCreateTask} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Title *
              </label>
              <input
                type="text"
                required
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                className="input-field"
                placeholder="Enter task title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                className="input-field"
                rows="3"
                placeholder="Enter task description (optional)"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Priority *
                </label>
                <select
                  value={newTask.priority}
                  onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
                  className="input-field"
                >
                  {PRIORITIES.map(priority => (
                    <option key={priority} value={priority}>
                      {priority.charAt(0).toUpperCase() + priority.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Label *
                </label>
                <select
                  value={newTask.label}
                  onChange={(e) => setNewTask({ ...newTask, label: e.target.value })}
                  className="input-field"
                >
                  {LABELS.map(label => (
                    <option key={label} value={label}>
                      {label.charAt(0).toUpperCase() + label.slice(1)}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reminder Time (Optional)
              </label>
              <input
                type="datetime-local"
                value={newTask.reminder_time}
                onChange={(e) => setNewTask({ ...newTask, reminder_time: e.target.value })}
                className="input-field"
              />
            </div>

            <button type="submit" className="btn-primary">
              Create Task
            </button>
          </form>
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="card text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks yet</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {tasks.map((task) => (
            <div key={task.id} className={`card hover:shadow-lg transition-shadow border-l-4 ${PRIORITY_COLORS[task.priority] || PRIORITY_COLORS.medium}`}>
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <input
                    type="checkbox"
                    checked={task.is_done}
                    onChange={() => handleToggleTask(task.id, task.is_done)}
                    className="mt-1 h-5 w-5 text-primary-600 rounded focus:ring-primary-500"
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className={`text-lg font-semibold ${task.is_done ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                        {task.title}
                      </h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${LABEL_COLORS[task.label] || LABEL_COLORS.other}`}>
                        {task.label}
                      </span>
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        task.priority === 'high' ? 'bg-red-500 text-white' : 
                        task.priority === 'medium' ? 'bg-yellow-500 text-white' : 
                        'bg-green-500 text-white'
                      }`}>
                        {task.priority}
                      </span>
                    </div>
                    {task.description && (
                      <p className={`mt-1 text-sm ${task.is_done ? 'text-gray-400' : 'text-gray-600'}`}>
                        {task.description}
                      </p>
                    )}
                    {task.reminder_time && (
                      <p className="mt-2 text-xs text-gray-500">
                        🔔 Reminder: {new Date(task.reminder_time).toLocaleString()}
                      </p>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="ml-4 text-red-600 hover:text-red-800 transition-colors"
                  title="Delete task"
                >
                  <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-8 text-center text-sm text-gray-500">
        {tasks.length > 0 && (
          <p>
            {tasks.filter(t => t.is_done).length} of {tasks.length} tasks completed
          </p>
        )}
      </div>
    </div>
  )
}
