document.addEventListener("DOMContentLoaded", () => {
    const projectList = document.getElementById("projectList");
    const projectForm = document.getElementById("projectForm");

    
    // Функция загрузки списка добавляемых проектов
    function loadProjects() {
        fetch("/api/portfolio")
            .then(response => response.json())
            .then(portfolio => {
                projectList.innerHTML = "";
                portfolio.forEach(project => {
                    const li = document.createElement("li");
                    li.innerHTML = `${project.title}. \nСсылка: ${project.link}
                        <button onclick="deleteProject(${project.id})">Удалить</button>`;
                    
                    projectList.appendChild(li);
                });
            });
    }


    // Добавление записи о новом проекте
    projectForm.addEventListener("submit", event => {
        event.preventDefault();
        const title = document.getElementById("title").value;
        const link = document.getElementById("link").value;

        fetch("/api/portfolio", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, link })
        }).then(response => response.json())
          .then(() => {
              projectForm.reset();
              loadProjects();
          });
    });

    // Удаление записи о проекте
    window.deleteProject = (id) => {
        fetch(`/api/portfolio/${id}`, { method: "DELETE" }).then(() => loadProjects());
    };


    // Загрузка проектов при загрузке страницы
    loadProjects();

});