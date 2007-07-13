from qt import *
import os.path

dir = os.path.dirname(__file__) + "/icons/"
dlg_zoom = dir + "Dlg_zoom.png"
dlg_pan = dir + "Dlg_zoom.png"
dlg_select = dir + "Dlg_zoom.png"
dlg_rect = dir + "Dlg_rect.png"
dlg_poly = dir + "Dlg_poly.png"

dlg_undo = dir + "Dlg_undo.png"
dlg_clear = dir + "Dlg_clear.png"
dlg_send = dir + "Dlg_send.png"
dlg_browseRectangle = dir + "Dlg_browseRectangle.png"
dlg_browseCircle = dir + "Dlg_browseCircle.png"

def createButton(parent, text, action = None, icon = None, toggle = 0):
    btn = QToolButton(parent)
    btn.setToggleButton(toggle)
    btn.cback = action   # otherwise garbage collection kills it
    if action: parent.connect(btn, SIGNAL("clicked()"), action)
    if icon:   btn.setPixmap(icon)
    QToolTip.add(btn, text)
    return btn
    
class ZoomSelectToolbar(QHButtonGroup):
#                (tooltip, attribute containing the button, callback function, button icon, button cursor, toggle)
    builtinFunctions = (None,
                 ("Zooming", "buttonZoom", "activateZooming", QPixmap(dlg_zoom), Qt.sizeAllCursor, 1), 
                 ("Panning", "buttonPan", "activatePanning", QPixmap(dlg_pan), Qt.pointingHandCursor, 1), 
                 ("Selection", "buttonSelect", "activateSelection", QPixmap(dlg_select), Qt.arrowCursor, 1), 
                 ("Rectangle selection", "buttonSelectRect", "activateRectangleSelection", QPixmap(dlg_rect), Qt.arrowCursor, 1), 
                 ("Polygon selection", "buttonSelectPoly", "activatePolygonSelection", QPixmap(dlg_poly), Qt.arrowCursor, 1), 
                 ("Remove last selection", "buttonRemoveLastSelection", "removeLastSelection", QPixmap(dlg_undo), None, 0), 
                 ("Remove all selections", "buttonRemoveAllSelections", "removeAllSelections", QPixmap(dlg_clear), None, 0), 
                 ("Send selections", "buttonSendSelections", "", QPixmap(dlg_send), None, 0)
                )
                 
    IconSpace, IconZoom, IconPan, IconSelect, IconRectangle, IconPolygon, IconRemoveLast, IconRemoveAll, IconSendSelection = range(9)

    def __init__(self, widget, parent, graph, autoSend = 0, buttons = (1, 4, 5, 0, 6, 7, 8)):
        QHButtonGroup.__init__(self, "Zoom / Select", parent)
        
        self.graph = graph # save graph. used to send signals
        self.widget = None
        
        self.functions = [type(f) == int and self.builtinFunctions[f] or f for f in buttons]
        for b, f in enumerate(self.functions):
            if not f:
                self.addSpace(10)
            else:
                button = createButton(self, f[0], lambda x=b: self.action(x), f[3], toggle = f[5])
                setattr(self, f[1], button)
                if f[0] == "Send selections":
                    button.setEnabled(not autoSend)

        self.action(0)
        self.widget = widget    # we set widget here so that it doesn't affect the value of self.widget.toolbarSelection

    def action(self, b):
        f = self.functions[b]
        if f[5]:
            if hasattr(self.widget, "toolbarSelection"):
                self.widget.toolbarSelection = b
            for fi, ff in enumerate(self.functions):
                if ff and ff[5]:
                    getattr(self, ff[1]).setOn(fi == b)
        getattr(self.graph, f[2])()
        
        # why doesn't this work?
        cursor = f[4]
        if not cursor is None:
            self.graph.canvas().setCursor(cursor)
            print self.graph.canvas().cursor().shape()
            if self.widget:
                self.widget.setCursor(cursor)
            
        
    # for backward compatibility with a previous version of this class
    def actionZooming(self): self.action(0)
    def actionRectangleSelection(self): self.action(3)
    def actionPolygonSelection(self): self.action(4)
    