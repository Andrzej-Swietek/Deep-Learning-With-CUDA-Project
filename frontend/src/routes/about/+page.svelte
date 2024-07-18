<script>
	import HerosSection from '@components/HerosSection.svelte';
	import userIcon from '$lib/images/placeholder-user.jpg'
</script>

<svelte:head>
	<title>About</title>
	<meta name="description" content="About this app" />
</svelte:head>

<HerosSection />

<section class="w-full py-12 md:py-24 lg:py-32 flex justify-center">
	<div class="container px-4 md:px-6">
		<div class="flex flex-col items-center justify-center space-y-4 text-center mb-16">
			<div class="space-y-2">
				<h2 class="text-3xl font-bold tracking-tighter sm:text-5xl">Our Mission</h2>
				<p class="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
					Our mission is to empower artists, designers, and creatives of all kinds to explore new frontiers of
					visual expression. By harnessing the power of neural networks, we aim to democratize the creation of
					stunning, one-of-a-kind artworks that push the boundaries of what's possible.
				</p>
			</div>
		</div>
		<div class="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-2 lg:gap-12">
			<img
				src="/placeholder.svg"
				width="550"
				height="310"
				alt="Our Team"
				class="mx-auto aspect-video overflow-hidden rounded-xl object-cover object-center sm:w-full lg:order-last"
			/>
			<div class="flex flex-col justify-center space-y-4">
				<div class="space-y-2">
					<h2 class="text-3xl font-bold tracking-tighter sm:text-5xl mb-4">Meet the Team</h2>
					<p class="max-w-[600px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
						Our talented team of engineers, designers, and researchers are dedicated to pushing the boundaries
						of what's possible with neural style transfer. We're passionate about empowering creativity and
						democratizing the creation of stunning artworks.
					</p>
				</div>
				<div class="grid grid-cols-2 gap-4">
					<div class="flex flex-col items-center justify-center space-y-2 mt-8">
                <span class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full">
                  <img class="aspect-square h-full w-full" alt="Avatar" src={userIcon} />
                </span>
						<p class="text-sm font-medium">Andrzej Świętek</p>
						<p class="text-sm text-muted-foreground"></p>
					</div>
					<div class="flex flex-col items-center justify-center space-y-2">
                <span class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full">
                  <img class="aspect-square h-full w-full" alt="Avatar" src={userIcon} />
                </span>
						<p class="text-sm font-medium">Krzystof Konieczny</p>
						<p class="text-sm text-muted-foreground"></p>
					</div>
					<div class="flex flex-col items-center justify-center space-y-2 col-span-2">
                <span class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full">
                  <img class="aspect-square h-full w-full" alt="Avatar" src={userIcon} />
                </span>
						<p class="text-sm font-medium">Jan Kwiatkowski</p>
						<p class="text-sm text-muted-foreground"></p>
					</div>

				</div>
			</div>
		</div>
	</div>
</section>


<section class="w-full py-12 md:py-24 lg:py-32 bg-muted flex justify-center">
	<div class="container px-4 md:px-6">
		<div class="flex flex-col items-center justify-center space-y-4 text-center">
			<div class="space-y-2">
				<h2 class="text-3xl font-bold tracking-tighter sm:text-5xl">Our Technology</h2>
				<p class="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
					Our neural style transfer technology is built on the latest advancements in deep learning and computer
					vision. By leveraging powerful neural networks, we're able to extract the key features and structures
					of an input image, and then seamlessly blend them with the artistic style of a reference image.
				</p>
			</div>
		</div>
		<div class="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-2 lg:gap-12">
			<img
				src="/placeholder.svg"
				width="550"
				height="310"
				alt="Our Technology"
				style=""
				class="mx-auto aspect-video overflow-hidden rounded-xl object-cover object-center sm:w-full lg:order-last"
			/>
			<div class="flex flex-col justify-center space-y-4">
				<ul class="grid gap-6">
					<li>
						<div class="grid gap-1">
							<h3 class="text-xl font-bold">Content Extraction</h3>
							<p class="text-muted-foreground">
								Our algorithm analyzes the content of the input image, identifying key features and structures.
							</p>
						</div>
					</li>
					<li>
						<div class="grid gap-1">
							<h3 class="text-xl font-bold">Style Transfer</h3>
							<p class="text-muted-foreground">
								The style of the reference image is then applied to the content of the input image, creating a
								unique blend.
							</p>
						</div>
					</li>
					<li>
						<div class="grid gap-1">
							<h3 class="text-xl font-bold">Optimization</h3>
							<p class="text-muted-foreground">
								The output is continuously refined through an optimization process to ensure the best possible
								result.
							</p>
						</div>
					</li>
				</ul>
			</div>
		</div>
	</div>
</section>