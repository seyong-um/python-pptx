# encoding: utf-8

"""Graphic Frame shape and related objects.

A graphic frame is a common container for table, chart, smart art, and media
objects.
"""

from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.shapes.base import BaseShape
from pptx.shared import ParentedElementProxy
from pptx.table import Table


class GraphicFrame(BaseShape):
    """Container shape for table, chart, smart art, and media objects.

    Corresponds to a ``<p:graphicFrame>`` element in the shape tree.
    """

    @property
    def chart(self):
        """The |Chart| object containing the chart in this graphic frame.

        Raises |ValueError| if this graphic frame does not contain a chart.
        """
        if not self.has_chart:
            raise ValueError("shape does not contain a chart")
        return self.chart_part.chart

    @property
    def chart_part(self):
        """The |ChartPart| object containing the chart in this graphic frame."""
        rId = self._element.chart_rId
        chart_part = self.part.related_parts[rId]
        return chart_part

    @property
    def has_chart(self):
        """|True| if this graphic frame contains a chart object. |False| otherwise.

        When |True|, the chart object can be accessed using the ``.chart`` property.
        """
        return self._element.has_chart

    @property
    def has_table(self):
        """|True| if this graphic frame contains a table object, |False| otherwise.

        When |True|, the table object can be accessed using the `.table` property.
        """
        return self._element.has_table

    @property
    def ole_format(self):
        """Optional _OleFormat object for this graphic-frame shape.

        Raises `ValueError` on a GraphicFrame instance that does not contain an OLE
        object.

        An shape that contains an OLE object will have `.shape_type` of either
        `EMBEDDED_OLE_OBJECT` or `LINKED_OLE_OBJECT`.
        """
        if not self._element.has_oleobj:
            raise ValueError("not an OLE-object shape")
        return _OleFormat(self._element.graphicData, self._parent)

    @property
    def shadow(self):
        """Unconditionally raises |NotImplementedError|.

        Access to the shadow effect for graphic-frame objects is
        content-specific (i.e. different for charts, tables, etc.) and has
        not yet been implemented.
        """
        raise NotImplementedError("shadow property on GraphicFrame not yet supported")

    @property
    def shape_type(self):
        """Optional member of `MSO_SHAPE_TYPE` identifying the type of this shape.

        Possible values are `MSO_SHAPE_TYPE.CHART`, and `MSO_SHAPE_TYPE.TABLE`.

        This value is `None` when neither of these types apply, for example when the
        shape contains SmartArt.
        """
        if self.has_chart:
            return MSO_SHAPE_TYPE.CHART
        elif self.has_table:
            return MSO_SHAPE_TYPE.TABLE
        else:
            return None

    @property
    def table(self):
        """
        The |Table| object contained in this graphic frame. Raises
        |ValueError| if this graphic frame does not contain a table.
        """
        if not self.has_table:
            raise ValueError("shape does not contain a table")
        tbl = self._element.graphic.graphicData.tbl
        return Table(tbl, self)


class _OleFormat(ParentedElementProxy):
    """Provides attributes on an embedded OLE object."""
