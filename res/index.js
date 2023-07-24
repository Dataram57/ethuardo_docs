/*
================================================
|                                              |
|                  Navigation                  |
|                                              |
================================================
*/

const ToggleFolder = (header) => {
    //css
    header.classList.toggle('folder-opened');
    //hide/show
    header = header.parentNode.lastElementChild;
    header.hidden = !header.hidden;
};