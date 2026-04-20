<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-narrow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Заголовок -->
      <div class="mb-8">
        <h1 class="text-2xl font-semibold text-gray-900 mb-2">Создать новую статью</h1>
        <p class="text-sm text-gray-600">Поделитесь своими мыслями и идеями с сообществом</p>
      </div>

      <!-- Форма создания поста -->
      <form @submit.prevent="handleSubmit" class="space-y-8">
        <!-- Основная информация -->
        <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Основная информация</h2>
          
          <div class="space-y-6">
            <!-- Заголовок -->
            <div>
              <label class="block text-sm font-medium text-gray-700">
                Заголовок статьи <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.title"
                type="text"
                required
                maxlength="200"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.title }"
                placeholder="Введите заголовок статьи..."
              />
              <div v-if="errors.title" class="mt-1 text-xs text-red-600">{{ errors.title }}</div>
              <div class="mt-1 text-xs text-gray-500">
                {{ form.title.length }}/200 символов
              </div>
            </div>

            <!-- Категория -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Категория</label>
              <select
                v-model="form.category"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
                :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.category }"
              >
                <option value="">Выберите категорию</option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
              <div v-if="errors.category" class="mt-1 text-xs text-red-600">{{ errors.category }}</div>
            </div>

            <!-- Изображение -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Изображение</label>
              
              <!-- Превью изображения -->
              <div v-if="imagePreview" class="mb-4">
                <div class="relative inline-block">
                  <img
                    :src="imagePreview"
                    alt="Preview"
                    class="w-full max-w-md h-48 object-cover rounded-md border border-gray-200"
                  />
                  <button
                    type="button"
                    @click="removeImage"
                    class="absolute top-2 right-2 p-1 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors"
                  >
                    <XMarkIcon class="w-4 h-4" />
                  </button>
                </div>
              </div>

              <!-- Загрузка изображения -->
              <div class="flex items-center justify-center w-full">
                <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-md cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
                  <div class="flex flex-col items-center justify-center pt-5 pb-6">
                    <PhotoIcon class="w-8 h-8 mb-2 text-gray-400" />
                    <p class="mb-2 text-sm text-gray-500">
                      <span class="font-medium">Нажмите для загрузки</span> или перетащите файл
                    </p>
                    <p class="text-xs text-gray-500">PNG, JPG, WEBP до 10MB</p>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleImageChange"
                  />
                </label>
              </div>
              <div v-if="errors.image" class="mt-1 text-xs text-red-600">{{ errors.image }}</div>
            </div>
          </div>
        </div>

        <!-- Содержимое -->
        <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Содержимое статьи</h2>
          
          <!-- Редактор -->
          <div>
            <label class="block text-sm font-medium text-gray-700">
              Текст статьи <span class="text-red-500">*</span>
            </label>
            
            <!-- Панель инструментов -->
            <div class="border border-gray-300 rounded-t-md bg-gray-50 p-2 flex items-center space-x-2">
              <button type="button" @click="formatText('bold')" class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors" title="Жирный">
                <BoldIcon class="w-4 h-4" />
              </button>
              <button type="button" @click="formatText('italic')" class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors" title="Курсив">
                <ItalicIcon class="w-4 h-4" />
              </button>
              <div class="border-l border-gray-300 h-6"></div>
              <button type="button" @click="formatText('h2')" class="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors" title="Заголовок">H2</button>
              <button type="button" @click="formatText('quote')" class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors" title="Цитата">
                <ChatBubbleLeftIcon class="w-4 h-4" />
              </button>
              <div class="border-l border-gray-300 h-6"></div>
              <button type="button" @click="formatText('link')" class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-md transition-colors" title="Ссылка">
                <LinkIcon class="w-4 h-4" />
              </button>
            </div>

            <!-- Текстовая область -->
            <textarea
              ref="contentTextarea"
              v-model="form.content"
              required
              rows="15"
              class="block w-full px-3 py-2 border border-gray-300 rounded-b-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
              :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.content }"
              placeholder="Напишите содержимое статьи..."
              @keydown="handleKeydown"
            ></textarea>
            
            <div v-if="errors.content" class="mt-1 text-xs text-red-600">{{ errors.content }}</div>
            <div class="mt-1 text-xs text-gray-500 flex justify-between">
              <span>{{ form.content.length }} символов</span>
              <span class="text-gray-400">Минимум 100 символов</span>
            </div>
          </div>
        </div>

        <!-- Настройки публикации -->
        <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Настройки публикации</h2>
          
          <div class="space-y-4">
            <!-- Статус -->
            <div>
              <label class="block text-sm font-medium text-gray-700">Статус публикации</label>
              <div class="space-y-3">
                <label class="flex items-start">
                  <input v-model="form.status" type="radio" value="published" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 mt-1" />
                  <span class="ml-3 text-sm">
                    <span class="font-medium text-gray-900">Опубликовать</span>
                    <span class="text-gray-500 block">Статья будет доступна всем пользователям</span>
                  </span>
                </label>
                <label class="flex items-start">
                  <input v-model="form.status" type="radio" value="draft" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 mt-1" />
                  <span class="ml-3 text-sm">
                    <span class="font-medium text-gray-900">Сохранить как черновик</span>
                    <span class="text-gray-500 block">Статья будет сохранена, но не опубликована</span>
                  </span>
                </label>
              </div>
            </div>

            <!-- Разрешить комментарии -->
            <div class="pt-4 border-t border-gray-200">
              <div class="flex items-center">
                <input id="allow-comments" v-model="form.allowComments" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                <label for="allow-comments" class="ml-3 text-sm text-gray-700">Разрешить комментарии к статье</label>
              </div>
            </div>
          </div>
        </div>

        <!-- Общие ошибки -->
        <div v-if="errors.general" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          <div class="flex">
            <ExclamationTriangleIcon class="h-5 w-5 text-red-400 mr-2" />
            <span>{{ errors.general }}</span>
          </div>
        </div>

        <!-- Кнопки действий -->
        <div class="flex items-center justify-between sticky bottom-0 bg-gray-50 p-4 rounded-md border border-gray-200">
          <router-link
            to="/posts"
            class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
          >
            <ArrowLeftIcon class="w-4 h-4 mr-2" />
            Отмена
          </router-link>

          <div class="flex items-center space-x-3">
            <!-- Предпросмотр -->
            <button
              type="button"
              @click="showPreview = true"
              class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
              :disabled="!form.title || !form.content"
            >
              <EyeIcon class="w-4 h-4 mr-2" />
              Предпросмотр
            </button>

            <!-- Статус автосохранения -->
            <div v-if="isAutoSaving" class="flex items-center text-sm text-gray-500">
              <div class="inline-block w-4 h-4 border-2 border-gray-500 border-t-transparent rounded-full animate-spin mr-2"></div>
              Автосохранение...
            </div>
            <div v-else-if="lastSaved" class="text-sm text-gray-500">
              Сохранено {{ formatTime(lastSaved) }}
            </div>

            <!-- Кнопка отправки -->
            <button
              type="submit"
              :disabled="postsStore.isSubmitting || !form.title.trim() || !form.content.trim()"
              class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
              :class="{ 'opacity-50 cursor-not-allowed': postsStore.isSubmitting || !form.title.trim() || !form.content.trim() }"
            >
              <div v-if="postsStore.isSubmitting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
              <DocumentPlusIcon v-else class="w-4 h-4 mr-2" />
              {{ form.status === 'published' ? 'Опубликовать' : 'Сохранить черновик' }}
            </button>
          </div>
        </div>
      </form>

      <!-- Модальное окно предпросмотра -->
      <teleport to="body">
        <div v-if="showPreview" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="showPreview = false">
          <div class="bg-white rounded-md max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div class="p-6 border-b border-gray-200 flex items-center justify-between sticky top-0 bg-white">
              <div>
                <h3 class="text-lg font-semibold text-gray-900">Предварительный просмотр</h3>
                <p class="text-sm text-gray-500">Так будет выглядеть ваша статья</p>
              </div>
              <button @click="showPreview = false" class="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-50 transition-colors">
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>
            
            <div class="p-6">
              <article class="prose prose-sm md:prose-lg max-w-none text-gray-700">
                <div v-if="imagePreview" class="mb-6">
                  <img :src="imagePreview" alt="Preview" class="w-full h-64 object-cover rounded-md" />
                </div>
                <h1 class="text-2xl md:text-3xl font-semibold text-gray-900 mb-4">{{ form.title || 'Заголовок статьи' }}</h1>
                
                <div class="flex items-center space-x-4 text-gray-600 text-sm mb-6 pb-6 border-b border-gray-200">
                  <div class="flex items-center space-x-2">
                    <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                      {{ authStore.userInitials }}
                    </div>
                    <span>{{ authStore.userFullName || 'Автор' }}</span>
                  </div>
                  <span>•</span>
                  <span>{{ new Date().toLocaleDateString('ru-RU') }}</span>
                  <span v-if="selectedCategoryName" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-600">
                    {{ selectedCategoryName }}
                  </span>
                </div>
                
                <div v-html="formattedPreviewContent"></div>
              </article>
            </div>

            <div class="p-6 border-t border-gray-200 bg-gray-50">
              <div class="flex justify-end space-x-3">
                <button @click="showPreview = false" class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors">
                  Закрыть
                </button>
                <button @click="showPreview = false" class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 text-sm font-medium transition-colors">
                  Продолжить редактирование
                </button>
              </div>
            </div>
          </div>
        </div>
      </teleport>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostsStore } from '@/stores/posts'
import { useToast } from 'vue-toastification'
import {
  XMarkIcon,
  PhotoIcon,
  EyeIcon,
  ChatBubbleLeftIcon,
  ArrowLeftIcon,
  DocumentPlusIcon,
  LinkIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const BoldIcon = { /* ... оставил как было */ }
const ItalicIcon = { /* ... оставил как было */ }

export default {
  name: 'PostCreateView',
  components: {
    XMarkIcon, PhotoIcon, EyeIcon, ChatBubbleLeftIcon,
    ArrowLeftIcon, DocumentPlusIcon, LinkIcon, ExclamationTriangleIcon,
    BoldIcon, ItalicIcon
  },

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const postsStore = usePostsStore()
    const toast = useToast()

    const contentTextarea = ref(null)
    const showPreview = ref(false)
    const imagePreview = ref(null)
    const imageFile = ref(null)
    const isAutoSaving = ref(false)
    const lastSaved = ref(null)
    const autoSaveTimer = ref(null)

    const form = reactive({
      title: '',
      content: '',
      category: '',
      status: 'published',
      allowComments: true
    })

    const errors = ref({})

    const categories = computed(() => postsStore.categories)

    const selectedCategoryName = computed(() => {
      if (!form.category) return null
      const category = categories.value.find(cat => cat.id == form.category)
      return category?.name || null
    })

    const formattedPreviewContent = computed(() => {
      if (!form.content) {
        return '<p class="text-gray-500 italic">Содержимое статьи будет отображено здесь...</p>'
      }

      return form.content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^## (.*$)/gm, '<h2 class="text-2xl font-semibold text-gray-900 mt-8 mb-4">$1</h2>')
        .replace(/^### (.*$)/gm, '<h3 class="text-xl font-semibold text-gray-900 mt-6 mb-3">$1</h3>')
        .replace(/^> (.*$)/gm, '<blockquote class="border-l-4 border-gray-200 pl-4 italic text-gray-600 my-4">$1</blockquote>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-600 hover:text-blue-700 underline" target="_blank" rel="noopener noreferrer">$1</a>')
        .replace(/\n\n/g, '</p><p class="mb-4">')
        .replace(/\n/g, '<br>')
        .replace(/^/, '<p class="mb-4">')
        .replace(/$/, '</p>')
    })

    // ====================== Автосохранение ======================
    const startAutoSave = () => {
      if (autoSaveTimer.value) clearInterval(autoSaveTimer.value)
      autoSaveTimer.value = setInterval(() => {
        if (form.title.trim() && form.content.trim()) saveAsDraft(true)
      }, 30000)
    }

    const saveAsDraft = async (isAutoSave = false) => {
      if (!form.title.trim() || !form.content.trim()) return
      if (isAutoSave) isAutoSaving.value = true

      try {
        const formData = new FormData()
        formData.append('title', form.title.trim())
        formData.append('content', form.content.trim())
        formData.append('status', 'draft')
        if (form.category) formData.append('category', form.category)
        if (imageFile.value) formData.append('image', imageFile.value)

        await api.post('/api/v1/posts/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        if (isAutoSave) lastSaved.value = new Date()
      } catch (error) {
        console.error('Ошибка автосохранения:', error)
      } finally {
        if (isAutoSave) isAutoSaving.value = false
      }
    }

    // ====================== Обработчики ======================
    const handleImageChange = (event) => {
      const file = event.target.files[0]
      if (!file) return

      if (file.size > 10 * 1024 * 1024) {
        toast.error('Размер файла не должен превышать 10MB')
        return
      }
      if (!file.type.startsWith('image/')) {
        toast.error('Можно загружать только изображения')
        return
      }

      imageFile.value = file
      const reader = new FileReader()
      reader.onload = (e) => { imagePreview.value = e.target.result }
      reader.readAsDataURL(file)
    }

    const removeImage = () => {
      imagePreview.value = null
      imageFile.value = null
    }

    const formatText = (format) => { /* ... твой код formatText без изменений ... */ }
    const handleKeydown = (event) => { /* ... твой код handleKeydown без изменений ... */ }

    const validateForm = () => {
      const newErrors = {}
      if (!form.title.trim()) newErrors.title = 'Заголовок обязателен'
      else if (form.title.length > 200) newErrors.title = 'Заголовок не должен превышать 200 символов'

      if (!form.content.trim()) newErrors.content = 'Содержимое статьи обязательно'
      else if (form.content.length < 100) newErrors.content = 'Статья должна содержать минимум 100 символов'

      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }

    // ====================== Основной submit ======================
    const handleSubmit = async () => {
      errors.value = {}

      if (!validateForm()) {
        toast.error('Пожалуйста, исправьте ошибки в форме')
        return
      }

      try {
        const postData = {
          title: form.title.trim(),
          content: form.content.trim(),
          status: form.status
        }
        if (form.category) postData.category = form.category

        const requestData = imageFile.value
          ? (() => {
              const fd = new FormData()
              Object.keys(postData).forEach(key => fd.append(key, postData[key]))
              fd.append('image', imageFile.value)
              return fd
            })()
          : postData

        const newPost = await postsStore.createPost(requestData)

        toast.success(
          form.status === 'published' ? 'Статья успешно опубликована!' : 'Черновик сохранен!'
        )

        // Очищаем таймер автосохранения
        if (autoSaveTimer.value) {
          clearInterval(autoSaveTimer.value)
        }

        // Безопасная навигация
        await nextTick()

        if (newPost?.slug) {
          router.push({ name: 'PostDetail', params: { slug: newPost.slug } })
        } else {
          router.push('/posts')
        }

      } catch (error) {
        console.error('Ошибка создания поста:', error)

        if (error.response?.status === 400) {
          const data = error.response.data || {}
          Object.keys(data).forEach(key => {
            errors.value[key] = Array.isArray(data[key]) ? data[key][0] : data[key]
          })
        } else {
          errors.value.general = 'Произошла ошибка при создании статьи. Попробуйте ещё раз.'
        }

        toast.error('Не удалось создать статью')
      }
    }

    const formatTime = (date) => { /* ... твой код formatTime без изменений ... */ }

    // ====================== Lifecycle ======================
    watch([() => form.title, () => form.content], () => {
      if (form.title.trim() && form.content.trim()) {
        startAutoSave()
      }
    })

    onMounted(async () => {
      if (categories.value.length === 0) {
        await postsStore.fetchCategories()
      }
      document.querySelector('input[type="text"]')?.focus()
    })

    onUnmounted(() => {
      if (autoSaveTimer.value) clearInterval(autoSaveTimer.value)
    })

    return {
      authStore,
      postsStore,
      form,
      errors,
      categories,
      selectedCategoryName,
      contentTextarea,
      showPreview,
      imagePreview,
      isAutoSaving,
      lastSaved,
      handleImageChange,
      removeImage,
      formatText,
      handleKeydown,
      handleSubmit,
      formatTime,
      saveAsDraft
    }
  }
}
</script>