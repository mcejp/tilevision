export const applyPageStyle = () => {
    document.head.append(document.createDocumentFragment(`<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;500;700&display=swap" rel="stylesheet">`))

    const body = document.getElementsByTagName("body")[0]
    body.classList.add("antialiased", "font-medium", "text-neutral-950", "bg-neutral-50")

    const style = document.createElement("style")
    style.textContent = `body {
        font-family: 'Inter', sans-serif;

        background-image: radial-gradient(#e5e5e5 12.5%, transparent 12.5%);
        background-size: 1rem 1rem;

        display: flex;
        justify-content: center;
        align-items: center;
    }`
    document.head.appendChild(style)
}

export const Btn = {
    props: {
        active: Boolean,
        padding: {type: String, default: "px-2.5"},
    },
    template: `
    <button type="button"
            class="border-2 border-solid border-indigo-700 mr-1 my-1 bg-neutral-50 text-indigo-700 hover:bg-indigo-700 hover:text-white rounded"
            :class="{'bg-indigo-200': active, 'border-indigo-600': active, 'btn-glow': active}"
            v-bind:class="padding"
            v-bind="$attrs"><slot/></button>
    `
}

export const PaneHeading = {
    template: `<div class="mb-1 pl-2 text-sm uppercase text-white bg-neutral-800 px-1.5 py-1 mx-[-0.5rem] font-bold"><slot/></div>`
}
  
export const PaneSubHeading = {
    template: `<div class="mb-1 text-center text-sm uppercase font-bold"><slot/></div>`
}
  
export const Pane = {
    template: `
    <div class="flex-none border-2 border-solid border-neutral-800 m-2 px-2 min-w-[12rem] rounded">
      <slot/>
    </div>
    `
}
