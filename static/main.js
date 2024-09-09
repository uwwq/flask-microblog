const paragraph = (block) => {
    return `<p>${block.data.text}</p>`;
};

const edjsParser = edjsHTML({paragraph});

const app = Vue.createApp({
    data() {
        return {
            posts: []
        };
    },
    methods: {
        async fetchPosts() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/posts');
                const data = await response.json();
                this.posts = data;
                console.log(this.posts);
            } catch (error) {
                console.error('Error fetching posts:', error);
            }
        },
        parsePost(post) {
            const editorjsData = JSON.parse(post.content);
            const html = edjsParser.parse(editorjsData);
            return html.join('');
        },
        formatDate(pubDate) {
            const postDate = new Date(pubDate);
            const now = new Date();
            const diffInMinutes = Math.floor((now - postDate) / (1000 * 60));
            const time_params = {
                hour: '2-digit',
                minute: '2-digit',
            };

            if (diffInMinutes < 60) {
                return `${postDate.toLocaleTimeString('ru-RU', time_params)}`;
            } else {
                return `${postDate.toLocaleDateString()} в ${postDate.toLocaleTimeString('ru-RU', time_params)}`;
            }
        }

    },
    mounted() {
        this.fetchPosts();
    }
});

app.mount('#app');