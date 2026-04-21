<template>
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
            class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-400 text-sm"
            :class="{ 'border-red-300 focus:border-red-500 focus:ring-red-500': errors.title }"
            placeholder="Введите заголовок статьи..."
            maxlength="200"
          />
          <div v-if="errors.title" class="mt-1 text-xs text-red-600">{{ errors.title }}</div>
          <div class="mt-1 text-xs text-gray-500">{{ form.title.length }}/200 символов</div>
        </div>

        <!-- Категория -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Категория</label>
          <select
            v-model="form.category"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 text-gray-900 text-sm"
          >
            <option value="">Выберите категорию</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <!-- Изображение -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Изображение</label>
          
          <!-- Превью -->
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
          
          <!-- Загрузка -->
          <div class="flex items-center justify-center w-full">
            <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-md cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
              <div class="flex flex-col items-center justify-center pt-5 pb-6">
                <PhotoIcon class="w-8 h-8 mb-2 text-gray-400" />
                <p class="mb-2 text-sm text-gray-500">
                  <span class="font-medium">Нажмите для загрузки</span> или перетащите файл
                </p>
                <p class="text-xs text-gray-500">PNG, JPG, WEBP до 10MB</p>
              </div>
              <input type="file" accept="image/*" class="hidden" @change="handleImageChange" />
            </label>
          </div>
          <div v-if="errors.image" class="mt-1 text-xs text-red-600">{{ errors.image }}</div>
        </div>
      </div>
    </div>

    <!-- Содержимое -->
    <div class="bg-white rounded-md shadow-sm border border-gray-200 p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Содержимое статьи</h2>
      
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
        <div>
          <label class="block text-sm font-medium text-gray-700">Статус публикации</label>
          <div class="space-y-3 mt-2">
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
      <button
        type="button"
        @click="$emit('cancel')"
        class="py-2 px-4 border border-gray-300 rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-700 text-sm font-medium transition-colors"
      >
        Отмена
      </button>
      
      <button
        type="submit"
        :disabled="postsStore.isSubmitting || !form.title.trim() || !form.content.trim()"
        class="py-2 px-4 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 text-sm font-medium transition-colors"
        :class="{ 'opacity-50 cursor-not-allowed': postsStore.isSubmitting || !form.title.trim() || !form.content.trim() }"
      >
        <div v-if="postsStore.isSubmitting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
        {{ isEditing ? 'Сохранить изменения' : (form.status === 'published' ? 'Опубликовать' : 'Сохранить черновик') }}
      </button>
    </div>
  </form>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { usePostsStore } from '@/stores/posts'
import { useToast } from 'vue-toastification'
import {
  XMarkIcon,
  PhotoIcon,
  ChatBubbleLeftIcon,
  LinkIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const BoldIcon = {
  template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M6 4v12c0 .55.45 1 1 1h4.5c2.49 0 4.5-2.01 4.5-4.5 0-1.4-.65-2.64-1.67-3.45.39-.82.67-1.69.67-2.55C15 4.01 12.99 2 10.5 2H7c-.55 0-1 .45-1 1v1zm2 2h2.5c.83 0 1.5.67 1.5 1.5S11.33 9 10.5 9H8V6zm0 5h3c.83 0 1.5.67 1.5 1.5S11.83 14 11 14H8v-3z"/></svg>'
}

const ItalicIcon = {
  template: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M8 2h6v2h-2l-2 8h2v2H6v-2h2l2-8H8V2z"/></svg>'
}

export default {
  name: 'PostFormComponent',
  components: {
    XMarkIcon,
    PhotoIcon,
    ChatBubbleLeftIcon,
    LinkIcon,
    ExclamationTriangleIcon,
    BoldIcon,
    ItalicIcon
  },
  props: {
    initialData: {
      type: Object,
      default: null
    },
    isEditing: {
      type: Boolean,
      default: false
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const postsStore = usePostsStore()
    const toast = useToast()
    
    const contentTextarea = ref(null)
    const imagePreview = ref(null)
    const imageFile = ref(null)
    const errors = ref({})
    
    const categories = computed(() => postsStore.categories)
    
    // Инициализируем форму с данными поста если редактируем
    const form = reactive({
      title: props.initialData?.title || '',
      content: props.initialData?.content || '',
      category: props.initialData?.category || '',
      status: props.initialData?.status || 'published',
    })
    
    // Если редактируем и есть изображение — показываем превью
    if (props.initialData?.image) {
      imagePreview.value = props.initialData.image
    }
    
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
      reader.onload = (e) => {
        imagePreview.value = e.target.result
      }
      reader.readAsDataURL(file)
    }
    
    const removeImage = () => {
      imagePreview.value = null
      imageFile.value = null
    }
    
    const formatText = (format) => {
      const textarea = contentTextarea.value
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selectedText = form.content.substring(start, end)
      
      let formattedText = ''
      let cursorOffset = 0
      
      switch (format) {
        case 'bold':
          formattedText = `**${selectedText}**`
          cursorOffset = selectedText ? 0 : 2
          break
        case 'italic':
          formattedText = `*${selectedText}*`
          cursorOffset = selectedText ? 0 : 1
          break
        case 'h2':
          formattedText = `## ${selectedText}`
          cursorOffset = selectedText ? 0 : 3
          break
        case 'quote':
          formattedText = `> ${selectedText}`
          cursorOffset = selectedText ? 0 : 2
          break
        case 'link':
          const url = selectedText.startsWith('http') ? selectedText : 'https://'
          const linkText = selectedText.startsWith('http') ? 'Текст ссылки' : selectedText || 'Текст ссылки'
          formattedText = `[${linkText}](${url})`
          cursorOffset = selectedText ? 0 : 1
          break
        default:
          formattedText = selectedText
      }
      
      form.content = form.content.substring(0, start) + formattedText + form.content.substring(end)
      
      setTimeout(() => {
        textarea.focus()
        const newPosition = start + formattedText.length - cursorOffset
        textarea.setSelectionRange(newPosition, newPosition)
      }, 0)
    }
    
    const handleKeydown = (event) => {
      if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
          case 'b':
            event.preventDefault()
            formatText('bold')
            break
          case 'i':
            event.preventDefault()
            formatText('italic')
            break
        }
      }
      
      if (event.key === 'Tab') {
        event.preventDefault()
        const start = event.target.selectionStart
        const end = event.target.selectionEnd
        form.content = form.content.substring(0, start) + '  ' + form.content.substring(end)
        setTimeout(() => {
          event.target.setSelectionRange(start + 2, start + 2)
        }, 0)
      }
    }
    
    const validateForm = () => {
      const newErrors = {}
      
      if (!form.title.trim()) {
        newErrors.title = 'Заголовок обязателен'
      } else if (form.title.length > 200) {
        newErrors.title = 'Заголовок не должен превышать 200 символов'
      }
      
      if (!form.content.trim()) {
        newErrors.content = 'Содержимое статьи обязательно'
      } else if (form.content.length < 100) {
        newErrors.content = 'Статья должна содержать минимум 100 символов'
      }
      
      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }
    
    const handleSubmit = async () => {
      errors.value = {}
      
      if (!validateForm()) {
        toast.error('Пожалуйста, исправьте ошибки в форме')
        return
      }
      
      try {
        const requestData = new FormData()
        requestData.append('title', form.title.trim())
        requestData.append('content', form.content.trim())
        requestData.append('status', form.status)
        
        if (form.category) {
          requestData.append('category', form.category)
        }
        
        if (imageFile.value) {
          requestData.append('image', imageFile.value)
        }
        
        emit('submit', requestData)
        
      } catch (error) {
        console.error('Ошибка формы:', error)
        errors.value.general = 'Произошла ошибка. Попробуйте еще раз.'
      }
    }
    
    onMounted(async () => {
      if (categories.value.length === 0) {
        await postsStore.fetchCategories()
      }
    })
    
    return {
      postsStore,
      form,
      errors,
      categories,
      contentTextarea,
      imagePreview,
      handleImageChange,
      removeImage,
      formatText,
      handleKeydown,
      handleSubmit
    }
  }
}
</script>