<script>

  export let data;

</script>

<h1>This is a basic implementation of a frontend for Postream.</h1>
<p>Visit <a href="https://github.com/dannowilby/postream">Postream's github page</a> to read the documentation</p>

{#each Object.values(data) as post}
  <h2>{post.title}</h2>
  <a href="/post/{post.url}">Read more</a>
{/each}
