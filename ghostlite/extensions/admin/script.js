fetch("/tables")
.then(r => r.json())
.then(data => {

    const list = document.getElementById("tables")

    data.forEach(t => {

        const li = document.createElement("li")

        li.innerText = t

        li.onclick = () => {

            fetch("/table/" + t)
            .then(r => r.json())
            .then(rows => console.log(rows))

        }

        list.appendChild(li)

    })

})