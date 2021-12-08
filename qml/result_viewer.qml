import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtWebEngine

ApplicationWindow {
    id: resultViewer
    
    // TODO: Insert web engine
    WebEngineView {
        id: webEngineView
        anchors.fill: parent
    }

    function show(cardToken) {
        visible = true
        searcher.selected_card_token = cardToken
        webEngineView.loadHtml(searcher.selected_card_html, "") // TODO: Use css file as the base URL
    }

    function hide() {
        visible = false
    }

}
