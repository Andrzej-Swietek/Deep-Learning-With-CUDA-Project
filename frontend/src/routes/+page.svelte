<script>
  import HerosSection from '@components/HerosSection.svelte';
  import OutputExamples from '@components/OutputExamples.svelte';
  import HowItWorksSection from '@components/HowItWorksSection.svelte';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Neural Style Transfer" />
</svelte:head>

  <HerosSection />
  <OutputExamples />
  <HowItWorksSection />
  <section class="w-full py-12 md:py-24 lg:py-32 flex justify-center items-center">
    <div class="container grid items-center justify-center gap-4 px-4 text-center md:px-6">
      <div class="space-y-3">
        <h2 class="text-3xl font-bold tracking-tighter md:text-4xl/tight">Start Creating Stunning Artworks</h2>
        <p class="mx-auto max-w-[600px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
          Upload your content and style images, and let our neural style transfer technology do the rest.
        </p>
      </div>
      <div class="mx-auto w-full max-w-sm space-y-2">
        <form class="flex flex-col gap-2">
          <div class="flex gap-2">
            <input
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 max-w-lg flex-1"
              placeholder="Upload content image"
              accept="image/png, image/jpeg"
              type="file"
            />
            <input
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 max-w-lg flex-1"
              placeholder="Upload style image"
              accept="image/png, image/jpeg"
              type="file"
            />
          </div>
          <button
            class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
            type="submit"
          >
            Transform
          </button>
        </form>
        <p class="text-xs text-muted-foreground">No registration required. Try it now for free.</p>
      </div>
    </div>
  </section>

