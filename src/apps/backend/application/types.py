from typing import Union, Optional

from werkzeug.sansio.response import Response

JSONResponse = tuple[Response, int]
RedirectResponse = Response
RedirectResponseOptional = Optional[Response]
RedirectRenderResponse = Union[Response, str]
