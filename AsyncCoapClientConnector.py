    # -------------------------
    # OBSERVE SUPPORT
    # -------------------------

    def startObserver(self, resource: str = None, name: str = None, ttl: int = 30) -> bool:
        if resource or name:
            resource_path = self._createResourcePath(resource, name)

            if not hasattr(self, "observeTasks"):
                self.observeTasks = {}
            if resource_path in self.observeTasks:
                logging.warning(f"Already observing resource {resource_path}. Ignoring start observe request.")
                return False

            full_uri = asyncio.run(self._build_uri(resource_path))

            task = asyncio.run_coroutine_threadsafe(
                self._handleStartObserveRequest(full_uri),
                asyncio.get_event_loop()
            )

            self.observeTasks[resource_path] = task
            logging.info(f"Started observing: {resource_path}")
            return True
        else:
            logging.warning("Can't issue Async OBSERVE - GET - no path provided.")
            return False

    def stopObserver(self, resource: str = None, name: str = None) -> bool:
        if resource or name:
            resource_path = self._createResourcePath(resource, name)

            if not hasattr(self, "observeTasks") or resource_path not in self.observeTasks:
                logging.warning(f"Resource {resource_path} not being observed. Ignoring stop observe request.")
                return False

            task = self.observeTasks[resource_path]
            task.cancel()

            cleanup_future = asyncio.run_coroutine_threadsafe(
                self._handleStopObserveRequest(resource_path, ignoreErr=True),
                asyncio.get_event_loop()
            )

            try:
                cleanup_future.result(timeout=5.0)
                logging.info(f"Stopped observing: {resource_path}")
                del self.observeTasks[resource_path]
                return True
            except Exception as e:
                logging.error(f"Error stopping observation: {e}")
                return False
        else:
            logging.warning("Can't cancel OBSERVE - GET - no path provided.")
            return False

    async def _handleStartObserveRequest(self, full_uri: str = None):
        logging.info(f"Handle start observe invoked. Waiting for updates: {full_uri}")
        try:
            msg = Message(code=Code.GET, uri=full_uri, observe=0)
            req = self.client_context.request(msg)

            if not hasattr(self, "observeRequests"):
                self.observeRequests = {}
            relative_path = full_uri.replace(self.base_url + "/", "")
            self.observeRequests[relative_path] = req

            # initial response
            responseData = await req.response
            self._onGetResponse(responseData)

            # continue observation
            async for responseData in req.observation:
                self._onGetResponse(responseData)

        except asyncio.CancelledError:
            logging.info(f"Observation cancelled for {full_uri}")
        except Exception as e:
            logging.warning(f"Failed to execute OBSERVE - GET. Error: {e}")
        finally:
            relative_path = full_uri.replace(self.base_url + "/", "")
            if relative_path in self.observeRequests:
                del self.observeRequests[relative_path]

    async def _handleStopObserveRequest(self, resource_path: str = None, ignoreErr: bool = False):
        if hasattr(self, "observeRequests") and resource_path in self.observeRequests:
            logging.info(f"Handle stop observe invoked: {resource_path}")
            try:
                observeRequest = self.observeRequests[resource_path]
                observeRequest.observation.cancel()
            except Exception as e:
                if not ignoreErr:
                    logging.warning(f"Failed to cancel OBSERVE - GET: {resource_path}")
            try:
                del self.observeRequests[resource_path]
            except Exception as e:
                if not ignoreErr:
                    logging.warning(f"Failed to remove observable from list: {resource_path}")
        else:
            if not ignoreErr:
                logging.warning(f"Resource not currently under observation. Ignoring: {resource_path}")

    def _onGetResponse(self, responseData):
        if not responseData or not responseData.payload:
            logging.warning("GET/OBSERVE response invalid. Ignoring.")
            return
        msg = responseData.payload.decode('utf-8')
        logging.info(f"OBSERVE/GET response received: {msg}")
