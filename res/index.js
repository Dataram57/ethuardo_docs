/*
================================================
|                                              |
|                  Navigation                  |
|                                              |
================================================
*/

const ToggleFolder = (header) => {
    const tag = header.parentNode.children[2];
    tag.hidden = !tag.hidden;
};