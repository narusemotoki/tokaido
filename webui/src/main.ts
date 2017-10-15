let ajax = (method: string, url: string, data: any, success_callback=null) => {
    let xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.addEventListener('loadend', () => {
        if(200 <= xhr.status && xhr.status < 300) {
            if (success_callback !== null ) {
                success_callback(JSON.parse(xhr.response));
            }
        } else {
            console.error(xhr.status, xhr.statusText);
        }
    });
    if (data !== null) {
        xhr.send(JSON.stringify(data));
    } else {
        xhr.send();
    }
};

class Main {
    private selectedId;
    private unselectedStyle;

    constructor() {
        this.selectedId = null;
        this.unselectedStyle = null;
    }

    main = () => {
        document.getElementById('new-step-button').onclick = () => {
            let title = window.prompt("Input title", "");
            if (title !== "" && title !== null) {
                let xhr = new XMLHttpRequest();
                xhr.open("POST", "/api/steps", true);
                xhr.onreadystatechange = function() {
                    let DONE = 4;
                    if (this.readyState !== DONE) {
                        return;
                    }
                    location.reload();
                }
                let data = JSON.stringify({"title": title});
                xhr.send(data);
            }
        }
        mermaid.initialize({startOnLoad: true, theme: 'forest'});
    }

    unselect = (rect) => {
        rect.style.stroke = this.unselectedStyle[0];
        rect.style.strokeWidth = this.unselectedStyle[1];
        this.selectedId = null;
    }

    _select = (id, rect) => {
        this.selectedId = id;
        this.unselectedStyle = [rect.style.stroke, rect.style.strokeWidth];
        rect.style.stroke = "#CC6699";
        rect.style.strokeWidth = "5";
    }

    set_relation = (id, rect) => {
        let next_step_id = parseInt(id.substring(2), 10);
        let path = "/api/steps/" + this.selectedId.substring(2);
        ajax(
            "GET",
            path,
            {},
            (step) => {
                console.log(step);
                step.next_step_ids.forEach((existing_id: number) => {
                    console.log(existing_id, next_step_id);
                    if (existing_id === next_step_id) {
                        location.reload();
                    }
                });
                step.next_step_ids.push(next_step_id);
                ajax(
                    "PUT",
                    path,
                    {
                        'title': step.title,
                        'next_step_ids': step.next_step_ids,
                    },
                    (step) => {
                        location.reload();
                    }
                );
            }
        )
    }

    select = (id: string) => {
        let target = document.getElementById(id);
        let rect = target.getElementsByTagName('rect')[0];
        if (this.selectedId === id) {
            this.unselect(rect);
        } else if (this.selectedId === null) {
            this._select(id, rect);
        } else {
            this.set_relation(id, rect);
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    let main = new Main();
    window.select = main.select;
    main.main();
});
