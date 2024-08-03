<script>
	import vader from '$lib/images/vader_vangogh.jpg'
</script>

<section class="w-full py-12 md:py-24 lg:py-32 bg-muted flex justify-center items-center">
	<div class="container px-4 md:px-6 grid gap-6 lg:grid-cols-2 lg:gap-12">
		<div class="flex flex-col justify-center space-y-4">
			<div class="space-y-2">
				<h1 class="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none">
					Transform Your Images with Neural Style Transfer
				</h1>
				<p class="max-w-[600px] text-muted-foreground md:text-xl">
					Our cutting-edge neural style transfer technology allows you to seamlessly blend the content of one
					image with the style of another, creating stunning and unique artworks.
				</p>
			</div>
			<div class="flex flex-col gap-2 min-[400px]:flex-row">
				<a
					href="/style-transfer"
					class="inline-flex h-10 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
				>
					Try it Now
				</a>
				<a
					href="#"
					class="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
				>
					Learn More
				</a>
			</div>
		</div>
		<img
			src={vader}

			style=""
			alt="Hero"
			class="mx-auto aspect-video overflow-hidden rounded-xl object-cover sm:w-full lg:order-last lg:aspect-square"
		/>
	</div>
</section>