app.get('/download/vscode', (req, res) => {
    const url = "https://code.visualstudio.com/sha/download?build=stable";
    fetch(url).then(response => {
        res.setHeader("Content-Disposition", "attachment; filename=vscode.exe");
        response.body.pipe(res);
    });
});
